// ─── Departures API Endpoint ──────────────────────────────────────────────────
// Cloudflare Pages Function: /api/salidas
// Fetches the latest departures.json directly from the GitHub repository API.
// This guarantees that the public site always shows live data, bypassing Pages build delays.

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET,OPTIONS',
  'Content-Type': 'application/json;charset=UTF-8',
  'Cache-Control': 'no-cache, no-store, must-revalidate',
};

export async function onRequestGet(context) {
  const { env } = context;
  
  // URL to fetch raw JSON content via GitHub API
  const url = `https://api.github.com/repos/manujungleforever-debug/manujungleforever/contents/www.manujungleforever.com/data/departures.json`;
  
  const token = env.GH_TOKEN || env.GITHUB_TOKEN;
  
  try {
    const res = await fetch(url, {
      headers: {
        'User-Agent': 'Cloudflare-Worker',
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/vnd.github.v3+json'
      }
    });

    if (!res.ok) {
      const errText = await res.text();
      console.error('GitHub API error:', errText);
      return new Response(JSON.stringify({ error: 'Failed to fetch departures' }), { 
        status: 500, 
        headers: CORS_HEADERS 
      });
    }

    const json = await res.json();
    
    // GitHub API returns content in Base64
    const base64Content = json.content.replace(/\n/g, '');
    const bytes = Uint8Array.from(atob(base64Content), c => c.charCodeAt(0));
    const decodedContent = new TextDecoder('utf-8').decode(bytes);
    
    // Parse it to ensure it's valid JSON and to optionally strip sensitive fields if needed.
    // For now, we return the parsed data as string.
    const departuresData = JSON.parse(decodedContent);

    // Filter out passengers data for public API security
    if (departuresData.salidas && Array.isArray(departuresData.salidas)) {
      departuresData.salidas = departuresData.salidas.map(s => {
        const { pasajeros, ...publicFields } = s;
        return publicFields;
      });
    }

    return new Response(JSON.stringify(departuresData), { 
      status: 200, 
      headers: CORS_HEADERS 
    });

  } catch (error) {
    console.error('API Error:', error);
    return new Response(JSON.stringify({ error: 'Internal server error' }), { 
      status: 500, 
      headers: CORS_HEADERS 
    });
  }
}

export async function onRequestOptions() {
  return new Response(null, { headers: CORS_HEADERS });
}
