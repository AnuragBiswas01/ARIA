import { createLazyFileRoute } from '@tanstack/react-router'

export const Route = createLazyFileRoute('/chat')({
  component: RouteComponent,
})

function RouteComponent() {
  return <div class="bg-white" >Hello "/chat"!</div>
}
