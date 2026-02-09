import { createLazyFileRoute } from '@tanstack/react-router'

export const Route = createLazyFileRoute('/memory')({
  component: RouteComponent,
})

function RouteComponent() {
  return <div>Hello "/memory"!</div>
}
