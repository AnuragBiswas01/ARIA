/**
 * System Store - Manages system status and health.
 */
import { create } from "zustand";
import { getSystemStatus, getSystemHealth } from "../services/api";

export const useSystemStore = create((set) => ({
  status: null,
  health: null,
  isOnline: false,
  isLoading: false,
  error: null,

  fetchStatus: async () => {
    set({ isLoading: true, error: null });
    try {
      const status = await getSystemStatus();
      set({
        status,
        isOnline: status.status === "online",
        isLoading: false,
      });
      return status;
    } catch (error) {
      set({
        isOnline: false,
        isLoading: false,
        error: error.message,
      });
      throw error;
    }
  },

  fetchHealth: async () => {
    try {
      const health = await getSystemHealth();
      set({ health, isOnline: health.status === "ok" });
      return health;
    } catch (error) {
      set({ isOnline: false });
      throw error;
    }
  },

  setOnline: (online) => set({ isOnline: online }),
}));
