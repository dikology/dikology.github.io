// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: 'My Docs',
			social: {
				github: 'https://github.com/withastro/starlight',
			},
			sidebar: [
				{
					label: 'Blog-ish',
					autogenerate: { directory: 'blog-ish' },
				},
				{
					label: 'Data',
					autogenerate: { directory: 'data' },
				},
				{
					label: 'Data Deck',
					autogenerate: { directory: 'data-deck' },
				},
				{
					label: 'Sailing',
					autogenerate: { directory: 'sailing' },
				},
				{
					label: 'Sailing Deck',
					autogenerate: { directory: 'sailing-deck' },
				},
				{
					label: 'Changelog',
					autogenerate: { directory: 'changelog' },
				},
			],
		}),
	],
});
