import { createLazyFileRoute } from '@tanstack/react-router'

export const Route = createLazyFileRoute('/automation')({
  component: RouteComponent,
})

function RouteComponent() {
  return <div>Hello "/automation"!</div>
}
