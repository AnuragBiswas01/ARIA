import { createLazyFileRoute } from '@tanstack/react-router'
import DevicesPage from '../pages/DevicesPage'

export const Route = createLazyFileRoute('/devices')({
  component: DevicesPage,
})
