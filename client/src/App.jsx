import { useEffect, useRef, useState, useCallback } from 'react';
import './App.css';

const MAX_VIDEOS = 16;
const MIN_VIDEOS = 1;

const App = () => {
  const videoRefs = useRef([]);
  const pcRefs = useRef({});
  const wsRef = useRef(null);
  const [isConnected, setIsConnected] = useState(false);
  const [streams, setStreams] = useState([]);
  const [connectionStates, setConnectionStates] = useState({});
  const [currentTime, setCurrentTime] = useState(new Date());

  // Update timestamp every second
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const createPeerConnection = useCallback((streamId) => {
    const pc = new RTCPeerConnection({
      iceServers: [{ urls: 'stun:stun.l.google.com:19302' }],
      iceCandidatePoolSize: 10,
      bundlePolicy: 'max-bundle',
      rtcpMuxPolicy: 'require'
    });

    pc.onicecandidate = (event) => {
      if (event.candidate && wsRef.current?.readyState === WebSocket.OPEN) {
        wsRef.current.send(JSON.stringify({
          type: 'ice',
          streamId: streamId,
          candidate: {
            sdpMid: event.candidate.sdpMid,
            sdpMLineIndex: event.candidate.sdpMLineIndex,
            candidate: event.candidate.candidate
          }
        }));
      }
    };

    pc.ontrack = (event) => {
      if (videoRefs.current[streamId]) {
        videoRefs.current[streamId].srcObject = event.streams[0];
      }
    };

    pc.onconnectionstatechange = () => {
      setConnectionStates(prev => ({
        ...prev,
        [streamId]: pc.connectionState
      }));
    };

    return pc;
  }, []);

  const startWebRTC = useCallback(async (streamId) => {
    try {
      const pc = createPeerConnection(streamId);
      pcRefs.current[streamId] = pc;

      pc.addTransceiver('video', { direction: 'recvonly' });

      const offer = await pc.createOffer();
      await pc.setLocalDescription(offer);

      if (wsRef.current?.readyState === WebSocket.OPEN) {
        wsRef.current.send(JSON.stringify({
          type: 'offer',
          streamId: streamId,
          sdp: pc.localDescription.sdp
        }));
      }
    } catch (error) {
      console.error(`WebRTC setup error for stream ${streamId}:`, error);
    }
  }, [createPeerConnection]);

  useEffect(() => {
    const connectWebSocket = () => {
      const ws = new WebSocket('ws://localhost:8000/ws/stream/');
      wsRef.current = ws;

      ws.onopen = () => {
        setIsConnected(true);
      };

      ws.onmessage = async (event) => {
        try {
          const message = JSON.parse(event.data);
          console.log('Received WebSocket message:', message); // Debug log

          if (message.type === 'stream_count') {
            // Ensure stream count is within limits
            const count = Math.max(MIN_VIDEOS, Math.min(message.count, MAX_VIDEOS));
            console.log('Setting up streams:', count);
            setStreams(Array(count).fill(null));
            // Start WebRTC connections for all streams
            Array(count).fill(null).forEach((_, index) => startWebRTC(index));
          } else if (message.type === 'answer' && pcRefs.current[message.streamId]) {
            await pcRefs.current[message.streamId].setRemoteDescription(
              new RTCSessionDescription({
                type: 'answer',
                sdp: message.sdp
              })
            );
          }
        } catch (error) {
          console.error('WebSocket message error:', error);
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setIsConnected(false);
      };

      ws.onclose = () => {
        setIsConnected(false);
        // Optional: Attempt to reconnect after a delay
        setTimeout(connectWebSocket, 5000);
      };

      return () => {
        Object.values(pcRefs.current).forEach(pc => pc.close());
        ws.close();
      };
    };

    connectWebSocket();
  }, [startWebRTC]);

  return (
    <div className="video-grid" data-streams={streams.length}>
      {streams.map((_, index) => (
        <div key={index} className="video-container">
          <video
            ref={el => videoRefs.current[index] = el}
            autoPlay
            playsInline
            muted
          />
          <div className={`video-overlay ${connectionStates[index] === 'connected' ? 'connected' : ''}`}>
            Camera {index + 1}
            <span className="connection-status">
              {connectionStates[index] || 'disconnected'}
            </span>
          </div>
          <div className={`connection-state ${connectionStates[index] === 'connected' ? 'connected' :
            connectionStates[index] === 'connecting' ? 'connecting' :
              'disconnected'
            }`} />
          <div className="timestamp">
            {currentTime.toLocaleTimeString()}
          </div>
        </div>
      ))}
    </div>
  );
};

export default App;
