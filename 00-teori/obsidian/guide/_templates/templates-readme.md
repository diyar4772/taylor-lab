---
title: Templates and Obsidian suggestions
tags: [guide, guide/template]
created: 2026-09-17
status: done
lang: en
---

# Templates and Obsidian suggestions

↑ [[00-START-HERE]] · Türkçe: [[sablonlar-hakkinda]]

The three files in this folder use the syntax of Obsidian's **built-in
Templates plugin** (`{{title}}`, `{{date}}`); no community plugin is needed.

| Template | When |
|---|---|
| [[session-log]] | At the end of each session in [[02-study-plan]] |
| [[experiment-log]] | When you try one of the "things to tinker with" in a layer note |
| [[concept-card]] | When you want to add your own concept to [[11-concept-map]] |

## Using them (in your vault, your choice)

This repository ships no `.obsidian/` settings. If you want to:

1. Enable *Settings → Core plugins → Templates*.
2. Set *Template folder location* = `00-teori/obsidian/guide/_templates`
   (if you opened the repo root as the vault).
3. Use the *Insert template* command in a new note.

With Templater, you can write `<% tp.date.now("YYYY-MM-DD") %>` instead of `{{date}}`.

## Graph view suggestion

Adding these queries as colour groups under *Graph view → Groups* makes the
guide's structure visible:

| Query | Meaning |
|---|---|
| `tag:#guide/moc` | entry point |
| `tag:#guide/plan` | study plan |
| `tag:#guide/layer` | the seven layer notes |
| `tag:#guide/result OR tag:#guide/concept` | results and concepts |
| `path:00-teori/obsidian -path:kilavuz -path:guide` | the repo's four atomic notes |
| `path:kilavuz` | Turkish version |

Using `path:00-teori/obsidian` as a filter hides source code and output files
from the graph.

Visual map: [[guide-map.canvas|Canvas]].
