import { useEffect, useRef } from "react";

const VideoGrid = () => {
    const videoRef = useRef(null);

    useEffect(() => {
        const ws = new WebSocket("ws://localhost:8000/ws/stream/");
        const mediaSource = new MediaSource();

        ws.onmessage = (event) => {
            if (videoRef.current && mediaSource.readyState === "open") {
                const buffer = videoRef.current.sourceBuffer;
                if (buffer && buffer.updating === false) {
                    buffer.appendBuffer(event.data);
                }
            }
        };

        if (videoRef.current) {
            videoRef.current.srcObject = mediaSource;
        }
    }, []);

    return (
        <div className="grid grid-cols-2 gap-4">
            <video ref={videoRef} autoPlay muted playsInline />
        </div>
    );
};

export default VideoGrid;
