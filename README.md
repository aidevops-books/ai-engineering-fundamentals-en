# AI Engineering Fundamentals — Companion Files

Official companion files for *AI Engineering Fundamentals* by John Bae (AIDevOps AI Engineering Series #01).
Every file the book refers to as `companion/...` is in this repository's `companion/` folder at the same path.

- Book page: <https://www.aidevops.us/books/>

## Getting the files

```bash
git clone https://github.com/aidevops-books/ai-engineering-fundamentals-en.git
cd ai-engineering-fundamentals-en/companion
```

## Layout

```text
companion/
├── shared/
├── v0_basic_model/
├── v1_llm_application/
├── v2_rag_application/
├── v3_agent_tools/
├── v4_mcp_integration/
├── v5_production_system/
├── README.md
└── requirements.txt
```

The lab order, prerequisites and what each file is for are in [`companion/README.md`](companion/README.md). Start there.

## Notes

- Use these files in a learning environment only. Passwords and tokens in the examples are teaching values, not for real services.
- With tool versions other than the book's, output and options may differ slightly.
- To report an error, open an Issue with the book title and edition, chapter, your environment and the steps to reproduce.

## License

Copyright © 2026 John Bae

- **Code** (manifests, Dockerfiles, scripts, configuration and example application source): [MIT License](LICENSE). Use and modify it freely, keeping the copyright notice.
- **Written guides** (every Markdown document, including this README): [CC BY-NC-ND 4.0](LICENSE-docs). Share them unchanged, with credit, for non-commercial purposes. Commands and code fragments quoted in the guides may be used under MIT, like the rest of the code.
- **The book's text and figures** are not in this repository. All rights reserved.

Software from other projects that the examples use, such as container images and Helm charts, remains under those projects' own licenses.
