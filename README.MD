# RTSP Streaming with WebRTC and Dynamic Grid

This project is a real-time RTSP streaming application that dynamically displays camera feeds in a responsive grid layout. Built using **React**, **Tailwind CSS**, **Django**, and **WebRTC**, it leverages **MediaMTX**, **FFmpeg**, and **WebSockets** for high-performance video streaming and scalability.

---

## **Workflow**

### **1. RTSP Stream Handling**
- RTSP streams from cameras are converted into WebRTC-compatible formats using **MediaMTX** and **FFmpeg**.
- Streams are broadcasted to multiple clients through a WebRTC-based **Pion SFU**, ensuring low-latency and scalable delivery.

### **2. Backend - Django**
- Django provides RESTful APIs to manage and fetch camera details.
- Handles user authentication and stores camera metadata.
- Manages WebSocket communication for signaling and real-time stream control.

### **3. Frontend - React**
- Fetches camera data via REST APIs and establishes WebRTC connections for live streaming.
- Displays streams in a responsive grid using **Tailwind CSS**.
- Allows users to add/remove cameras and control streaming settings dynamically.

### **4. WebSocket Communication**
- WebSockets enable real-time communication between the backend and frontend for:
  - Stream state updates.
  - Latency information.
  - Command signaling (e.g., start/stop streams).

### **5. Dynamic Grid Layout**
- The grid layout adjusts dynamically based on the number of active streams.
- Users can interact with individual streams (e.g., toggle fullscreen, stop stream).

---

## **Tech Stack**

### **Frontend**
- **React**: For building the dynamic UI.
- **Tailwind CSS**: For responsive and modern styling.

### **Backend**
- **Django**: As the backend framework for API and WebSocket management.
- **Django Channels**: For WebSocket support.

### **Streaming Tools**
- **MediaMTX**: To convert RTSP streams to WebRTC-compatible formats.
- **FFmpeg**: For transcoding and quality adjustments.
- **Pion WebRTC SFU**: For real-time scalable video delivery.

### **Other Tools**
- **FFplay**: For debugging RTSP streams.

---

## **Setup and Installation**

### **1. Prerequisites**
Ensure the following dependencies are installed on your system:
- Python 3.9 or above
- Node.js and npm
- FFmpeg
- MediaMTX
- Daphne (ASGI server for Django)

### **2. Clone the Repository**
```bash
git clone https://github.com/Sameer16536/RtspStreaming.git
cd RtspStreaming
```

### **3. Backend Setup**
Navigate to the backend directory:
```bash
cd backend
```

Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run database migrations:
```bash
python manage.py migrate
```

Start the Django ASGI server:
```bash
daphne -p 8000 server.asgi:application
```

### **4. Frontend Setup**
Navigate to the frontend directory:
```bash
cd ../frontend
```

Install dependencies:
```bash
npm install
```

Start the development server:
```bash
npm start
```

### **5. Media Server Setup**
Run MediaMTX to serve RTSP streams. Configure mediamtx.yml with your RTSP server settings.

Start streaming using FFmpeg:
```bash
ffmpeg -re -stream_loop -1 -i 1.mp4 -c:v libx264 -b:v 1.5M -maxrate 2M -bufsize 2M -preset ultrafast -tune zerolatency -f rtsp -rtsp_transport tcp rtsp://localhost:8554/live.sdp
```

Test the stream using FFplay:
```bash
ffplay rtsp://localhost:8554/live.sdp
```

## **Commands Summary**
| Command | Description |
|---------|-------------|
| `daphne -p 8000 server.asgi:application` | Starts the Django backend server |
| `npm start` | Starts the React frontend |
| `ffmpeg -re -stream_loop -1 -i 1.mp4 ...` | Streams RTSP video to MediaMTX |
| `ffplay rtsp://localhost:8554/live.sdp` | Tests the RTSP stream locally |

## **Features**
- Dynamic Grid Layout: Responsive design to display multiple camera streams
- WebSocket Integration: Real-time updates for camera state and stream latency
- Stream Control: Add/remove cameras, start/stop streams dynamically
- Low-Latency Streaming: Optimized for real-time video delivery using WebRTC

## **Future Enhancements**
- PTZ (Pan, Tilt, Zoom) controls for supported cameras
- Recording and playback of streams
- User authentication and role-based access control
- Enhanced analytics and monitoring (e.g., bandwidth usage, FPS stats)

## **Contributing**
Contributions are welcome! Feel free to submit issues or pull requests.

## **License**
This project is licensed under the MIT License.

