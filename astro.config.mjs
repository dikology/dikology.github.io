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
					label: 'Datafolio',
					autogenerate: { directory: 'datafolio' },
				},
				{
					label: 'Data Deck',
					autogenerate: { directory: 'data-deck' },
				},
				{
					label: 'Sailing',
					items: [
						{
							label: 'At home',
							autogenerate: { directory: 'sailing/at-home' },
						},
						{
							label: 'In the plane',
							autogenerate: { directory: 'sailing/in-the-plane' },
						},
						{
							label: 'In the marina',
							autogenerate: { directory: 'sailing/in-the-marina' },
						},
						{
							label: 'On the yacht',
							autogenerate: { directory: 'sailing/on-the-yacht' },
						},
						{
							label: 'Helpful info',
							autogenerate: { directory: 'sailing/helpful-info' },
						},
						{
							label: 'At sea',
							autogenerate: { directory: 'sailing/at-sea' },
						},
					],
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
