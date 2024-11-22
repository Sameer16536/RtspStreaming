import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCIceCandidate, RTCConfiguration, RTCIceServer
from aiortc.contrib.media import MediaPlayer
import asyncio
import gc

logger = logging.getLogger(__name__)

# Reduce number of simultaneous streams if needed
RTSP_STREAMS = [
    'rtsp://localhost:8554/live.sdp',
    'rtsp://localhost:8554/live.sdp',
    'rtsp://localhost:8554/live.sdp',
    'rtsp://localhost:8554/live.sdp',
    'rtsp://localhost:8554/live.sdp',
    'rtsp://localhost:8554/live.sdp',
    'rtsp://localhost:8554/live.sdp',
    'rtsp://localhost:8554/live.sdp',
    # 'rtsp://localhost:8554/live.sdp',
    # 'rtsp://localhost:8554/live.sdp',
    # 'rtsp://localhost:8554/live.sdp',
    # 'rtsp://localhost:8554/live.sdp',
    # 'rtsp://localhost:8554/live.sdp',
    # 'rtsp://localhost:8554/live.sdp',
    # 'rtsp://localhost:8554/live.sdp',
    # 'rtsp://localhost:8554/live.sdp',
    # ... other streams ...
]

class WebRTCConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.pcs = {}
        self.players = {}
        self.active_streams = set()  # Track active streams
        await self.accept()
        await self.send(json.dumps({
            'type': 'stream_count',
            'count': len(RTSP_STREAMS)
        }))

    async def receive(self, text_data):
        try:
            message = json.loads(text_data)
            stream_id = message.get('streamId')
            
            if message['type'] == 'offer':
                # Clean up existing connection if any
                await self.cleanup_stream(stream_id)

                config = RTCConfiguration([
                    RTCIceServer(urls=['stun:stun.l.google.com:19302'])
                ])
                pc = RTCPeerConnection(configuration=config)
                self.pcs[stream_id] = pc

                # Optimized MediaPlayer settings
                self.players[stream_id] = MediaPlayer(
                    RTSP_STREAMS[stream_id],
                    options={
                        'rtsp_transport': 'tcp',
                        'stimeout': '3000000',  # Reduced timeout
                        'fflags': 'nobuffer',
                        'flags': 'low_delay',
                        'buffer_size': '512000',  # Reduced buffer size
                        'reorder_queue_size': '0',
                        'max_delay': '500000',  # 0.5 second max delay
                        'thread_queue_size': '512',
                        'fps': '15',  # Limit FPS
                    }
                )

                @pc.on("connectionstatechange")
                async def on_connectionstatechange():
                    logger.info(f"Stream {stream_id} connection state: {pc.connectionState}")
                    if pc.connectionState == "failed":
                        await self.cleanup_stream(stream_id)
                    elif pc.connectionState == "connected":
                        self.active_streams.add(stream_id)

                if self.players[stream_id].video:
                    pc.addTrack(self.players[stream_id].video)

                # Handle offer/answer exchange
                await pc.setRemoteDescription(
                    RTCSessionDescription(
                        sdp=message['sdp'],
                        type=message['type']
                    )
                )
                
                answer = await pc.createAnswer()
                answer.sdp = answer.sdp.replace('a=sendrecv', 'a=sendonly')
                
                # Add bandwidth constraints to SDP
                answer.sdp = self.add_bandwidth_constraints(answer.sdp)
                
                await pc.setLocalDescription(answer)

                await self.send(json.dumps({
                    'type': 'answer',
                    'streamId': stream_id,
                    'sdp': pc.localDescription.sdp
                }))

            elif message['type'] == 'ice':
                if stream_id in self.pcs:
                    pc = self.pcs[stream_id]
                    candidate = RTCIceCandidate(
                        sdpMid=message['candidate']['sdpMid'],
                        sdpMLineIndex=message['candidate']['sdpMLineIndex'],
                        candidate=message['candidate']['candidate']
                    )
                    await pc.addIceCandidate(candidate)
                    
        except Exception as e:
            logger.error(f"Error in WebRTC consumer: {e}")
            logger.error(traceback.format_exc())
            await self.cleanup_stream(stream_id)

    def add_bandwidth_constraints(self, sdp):
        """Add bandwidth constraints to SDP"""
        lines = sdp.split('\n')
        modified_lines = []
        for line in lines:
            modified_lines.append(line)
            if line.startswith('m=video'):
                modified_lines.append('b=AS:800')  # 800 kbps
                modified_lines.append('b=TIAS:800000')
        return '\n'.join(modified_lines)

    async def cleanup_stream(self, stream_id):
        """Clean up resources for a specific stream"""
        try:
            if stream_id in self.pcs:
                await self.pcs[stream_id].close()
                del self.pcs[stream_id]
            
            if stream_id in self.players:
                self.players[stream_id].stop()
                del self.players[stream_id]
            
            if stream_id in self.active_streams:
                self.active_streams.remove(stream_id)
            
            # Force garbage collection
            gc.collect()
            
        except Exception as e:
            logger.error(f"Error cleaning up stream {stream_id}: {e}")

    async def disconnect(self, close_code):
        """Clean up all resources on disconnect"""
        try:
            for stream_id in list(self.pcs.keys()):
                await self.cleanup_stream(stream_id)
        except Exception as e:
            logger.error(f"Error during disconnect: {e}")
