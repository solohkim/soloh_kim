export default async (request, context) => {
  const url = new URL(request.url);
  if (url.pathname.startsWith('/certs/')) {
    const ref = request.headers.get('referer') || '';
    // Allow if coming from your own site (homepage OR viewer)
    if (ref.includes('kimsec.netlify.app')) {
      return context.next();
    }
    // Block if typed directly / no referer / from other site
    return new Response('Direct download disabled - use viewer', { status: 403 });
  }
  return context.next();
}
export const config = { path: "/certs/*" };