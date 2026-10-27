export default async (request, context) => {
  const url = new URL(request.url);
  if (url.pathname.startsWith('/certs/')) {
    const ref = request.headers.get('referer') || '';
    if (!ref.includes('viewer.html')) {
      return new Response('Direct download disabled - use viewer', { status: 403 });
    }
  }
  return context.next();
}
export const config = { path: "/certs/*" };