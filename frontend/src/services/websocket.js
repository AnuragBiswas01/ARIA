/**
 * ARIA WebSocket Service
 * Handles real-time event streaming from backend.
 */

const WS_BASE_URL = import.meta.env.VITE_WS_URL || "ws://localhost:8000";

class WebSocketService {
  constructor() {
    this.socket = null;
    this.listeners = new Map();
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 1000;
  }

  connect() {
    if (this.socket?.readyState === WebSocket.OPEN) {
      return;
    }

    try {
      this.socket = new WebSocket(`${WS_BASE_URL}/api/events/ws`);

      this.socket.onopen = () => {
        console.log("[WS] Connected");
        this.reconnectAttempts = 0;
        this.emit("connected", true);
      };

      this.socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.emit("message", data);

          if (data.type === "event") {
            this.emit("event", data.payload);
          }
        } catch (e) {
          console.error("[WS] Failed to parse message:", e);
        }
      };

      this.socket.onclose = () => {
        console.log("[WS] Disconnected");
        this.emit("connected", false);
        this.attemptReconnect();
      };

      this.socket.onerror = (error) => {
        console.error("[WS] Error:", error);
        this.emit("error", error);
      };
    } catch (error) {
      console.error("[WS] Connection failed:", error);
    }
  }

  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }

  attemptReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.log("[WS] Max reconnection attempts reached");
      return;
    }

    this.reconnectAttempts++;
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);

    console.log(
      `[WS] Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`,
    );
    setTimeout(() => this.connect(), delay);
  }

  send(data) {
    if (this.socket?.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(data));
    }
  }

  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event).push(callback);
  }

  off(event, callback) {
    const callbacks = this.listeners.get(event);
    if (callbacks) {
      const index = callbacks.indexOf(callback);
      if (index > -1) {
        callbacks.splice(index, 1);
      }
    }
  }

  emit(event, data) {
    const callbacks = this.listeners.get(event);
    if (callbacks) {
      callbacks.forEach((cb) => cb(data));
    }
  }
}

// Singleton instance
const websocketService = new WebSocketService();
export default websocketService;
