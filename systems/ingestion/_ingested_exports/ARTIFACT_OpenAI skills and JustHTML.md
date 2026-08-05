---
title: OpenAI skills and JustHTML
domain: 03_NEURAL_FOREST
source: gemini: 2025-12-22_025_openai-skills-and-justhtml.md
tags: gemini,archaeology,full-body
type: knowledge_artifact
---

# OpenAI skills and JustHTML
**Domain:** 03_NEURAL_FOREST
**Source:** gemini: 2025-12-22_025_openai-skills-and-justhtml.md

# OpenAI skills and JustHTML

> **Catalog #25** | Extracted 2026-06-16 04:03 UTC
> Created: 2025-12-22 06:49 UTC
> Updated: 2025-12-22 07:35 UTC

**16 messages**

---

### Message 5 — 👤 User

OpenAI are quietly adopting skills, now available in ChatGPT and Codex CLI
JustHTML is a fascinating example of vibe engineering in action

I ported JustHTML from Python to JavaScript with Codex CLI and GPT-5.2 in 4.5 hours

Plus 8 links and 4 quotations

Thanks for reading Simon Willison’s Newsletter! Subscribe for free to receive new posts and support my work.

Subscribe
If you find this newsletter useful, please consider sponsoring me via GitHub. $10/month and higher sponsors get a monthly newsletter with my summary of the most important trends of the past 30 days - here are previews from September and October.

OpenAI are quietly adopting skills, now available in ChatGPT and Codex CLI - 2025-12-12
One of the things that most excited me about Anthropic’s new Skills mechanism back in October is how easy it looked for other platforms to implement. A skill is just a folder with a Markdown file and some optional extra resources and scripts, so any LLM tool with the ability to navigate and read from a filesystem should be capable of using them. It turns out OpenAI are doing exactly that, with skills support quietly showing up in both their Codex CLI tool and now also in ChatGPT itself.

Skills in ChatGPT
I learned about this from Elias Judin this morning. It turns out the Code Interpreter feature of ChatGPT now has a new /home/oai/skills folder which you can access simply by prompting:

Create a zip file of /home/oai/skills

Screenshot of file explorer. Files skills/docs/render_docsx.py and skills/docs/skill.md and skills/pdfs/ and skills/pdfs/skill.md - that last one is expanded and reads: # PDF reading, creation, and review guidance  ## Reading PDFs - Use pdftoppm -png $OUTDIR/$BASENAME.pdf $OUTDIR/$BASENAME to convert PDFs to PNGs. - Then open the PNGs and read the images. - pdfplumber is also installed and can be used to read PDFs. It can be used as a complementary tool to pdftoppm but not replacing it. - Only do python printing as a last resort because you will miss important details with text extraction (e.g. figures, tables, diagrams).  ## Primary tooling for creating PDFs - Generate PDFs programmatically with reportlab as the primary tool. In most cases, you should use reportlab to create PDFs. - If there are other packages you think are necessary for the task (eg. pypdf, pyMuPDF), you can use them but you may need topip install them first. - After each meaningful update—content additions, layout adjustments, or style changes—render the PDF to images to check layout fidelity:   - pdftoppm -png $INPUT_PDF $OUTPUT_PREFIX - Inspect every exported PNG before continuing work. If anything looks off, fix the source and re-run the render → inspect loop until the pages are clean.  ## Quality expectations - Maintain a polished, intentional visual design: consistent typography, spacing, margins, color palette, and clear section breaks across all pages. - Avoid major rendering issues—no clipped text, overlapping elements, black squares, broken tables, or unreadable glyphs. The rendered pages should look like a curated document, not raw template output. - Charts, tables, diagrams, and images must be sharp, well-aligned, and properly labeled in the PNGs. Legends and axes should be readable without excessive zoom. - Text must be readable at normal viewing size; avoid walls of filler text or dense, unstructured bullet lists. Use whitespace to separate ideas. - Never use the U+2011 non-breaking hyphen or other unicode dashes as they will not be
So far they cover spreadsheets, docx and PDFs. Interestingly their chosen approach for PDFs and documents is to convert them to rendered per-page PNGs and then pass those through their vision-enabled GPT models, presumably to maintain information from layout and graphics that would be lost if they just ran text extraction.

Elias shared copies in a GitHub repo. They look very similar to Anthropic’s implementation of the same kind of idea, currently published in their anthropics/skills repository.

I tried it out by prompting:

Create a PDF with a summary of the rimu tree situation right now and what it means for kakapo breeding season

Sure enough, GPT-5.2 Thinking started with:

Reading skill.md for PDF creation guidelines

Then:

Searching rimu mast and Kākāpō 2025 breeding status

It took just over eleven minutes to produce this PDF, which was long enough that I had Claude Code for web build me a custom PDF viewing tool while I waited.

(I am very excited about Kākāpō breeding season this year.)

The reason it took so long is that it was fastidious about looking at and tweaking its own work. I appreciated that at one point it tried rendering the PDF and noticed that the macrons in kākāpō were not supported by the chosen font, so it switched to something else:

ChatGPT screenshot. Analyz
