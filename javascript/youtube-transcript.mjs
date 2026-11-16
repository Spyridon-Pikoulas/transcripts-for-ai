// Transcripts of YouTube videos from Node.js.
//   npm install && APIFY_TOKEN=... node youtube-transcript.mjs https://www.youtube.com/watch?v=dQw4w9WgXcQ
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('pikoulas/youtube-transcripts').call({
    videos: process.argv.slice(2),
    includeTimestamps: true, // adds `segments`: each line with its start and end in seconds
}, { log: null }); // log: null keeps the run's own log out of your console
const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const item of items) {
    console.log(`# ${item.title}\n${item.url}\n`);
    console.log(item.text ?? item.error, '\n');
}
