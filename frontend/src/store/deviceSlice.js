/**
 * Device Store - Manages smart home device state.
 */
import { create } from "zustand";
import { getDevices, controlDevice } from "../services/api";

export const useDeviceStore = create((set, get) => ({
  devices: [],
  isLoading: false,
  error: null,

  fetchDevices: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await getDevices();
      set({ devices: response.devices || [], isLoading: false });
      return response;
    } catch (error) {
      set({ isLoading: false, error: error.message });
      throw error;
    }
  },

  controlDevice: async (entityId, action, value = null) => {
    try {
      const response = await controlDevice(entityId, action, value);

      // Optimistically update local state
      if (response.status === "success" || response.status === "simulated") {
        set((state) => ({
          devices: state.devices.map((device) =>
            device.entity_id === entityId
              ? { ...device, state: action === "turn_on" ? "on" : "off" }
              : device,
          ),
        }));
      }

      return response;
    } catch (error) {
      set({ error: error.message });
      throw error;
    }
  },

  updateDeviceState: (entityId, state) => {
    set((current) => ({
      devices: current.devices.map((device) =>
        device.entity_id === entityId ? { ...device, state } : device,
      ),
    }));
  },
}));
