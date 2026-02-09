/**
 * Settings Store - User preferences and app settings.
 */
import { create } from "zustand";
import { persist } from "zustand/middleware";

export const useSettingsStore = create(
  persist(
    (set) => ({
      theme: "dark",
      sidebarCollapsed: false,
      notifications: true,
      soundEnabled: true,
      autoScroll: true,

      setTheme: (theme) => set({ theme }),
      toggleSidebar: () =>
        set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),
      setNotifications: (enabled) => set({ notifications: enabled }),
      setSoundEnabled: (enabled) => set({ soundEnabled: enabled }),
      setAutoScroll: (enabled) => set({ autoScroll: enabled }),
    }),
    {
      name: "aria-settings",
    },
  ),
);
