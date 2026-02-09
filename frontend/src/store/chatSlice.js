/**
 * Chat Store - Manages chat state and messages.
 */
import { create } from "zustand";
import { sendMessage } from "../services/api";

export const useChatStore = create((set, get) => ({
  messages: [],
  sessionId: null,
  isLoading: false,
  error: null,

  addMessage: (role, content, metadata = null) => {
    const message = {
      id: Date.now(),
      role,
      content,
      metadata,
      timestamp: new Date().toISOString(),
    };
    set((state) => ({ messages: [...state.messages, message] }));
    return message;
  },

  sendUserMessage: async (content) => {
    const state = get();
    set({ isLoading: true, error: null });

    // Add user message immediately
    state.addMessage("user", content);

    try {
      const response = await sendMessage(content, state.sessionId);

      // Update session ID if new
      if (response.session_id && !state.sessionId) {
        set({ sessionId: response.session_id });
      }

      // Add AI response
      state.addMessage("assistant", response.response, {
        toolCalls: response.tool_calls,
        toolResults: response.tool_results,
      });

      set({ isLoading: false });
      return response;
    } catch (error) {
      set({ isLoading: false, error: error.message });
      state.addMessage("system", `Error: ${error.message}`);
      throw error;
    }
  },

  clearMessages: () => set({ messages: [], sessionId: null, error: null }),

  setSessionId: (id) => set({ sessionId: id }),
}));
