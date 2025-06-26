# MkDocs.yml Configuration Template

Below is the complete `mkdocs.yml` configuration for the Enhanced Toolkits project:

```yaml
# Site Information
site_name: Enhanced Toolkits
site_description: Production-ready AI agent tools for developers building intelligent chatbots and AI systems
site_author: malvavisc0
site_url: https://malvavisc0.github.io/enhancedtoolkits

# Repository
repo_name: malvavisc0/enhancedtoolkits
repo_url: https://github.com/malvavisc0/enhancedtoolkits
edit_uri: edit/main/docs/

# Copyright
copyright: Copyright &copy; 2025 malvavisc0

# Configuration
theme:
  name: material
  language: en
  
  # Color palette
  palette:
    - scheme: default
      primary: blue
      accent: green
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: blue
      accent: green
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  
  # Fonts
  font:
    text: Roboto
    code: Roboto Mono
  
  # Logo and favicon
  logo: assets/images/logo.png
  favicon: assets/images/favicon.ico
  
  # Features
  features:
    - navigation.tabs
    - navigation.tabs.sticky
    - navigation.sections
    - navigation.expand
    - navigation.path
    - navigation.indexes
    - navigation.top
    - search.highlight
    - search.share
    - search.suggest
    - toc.follow
    - toc.integrate
    - content.code.copy
    - content.code.select
    - content.code.annotate
    - content.action.edit
    - content.action.view
    - announce.dismiss

# Plugins
plugins:
  - search:
      separator: '[\s\-,:!=\[\]()"`/]+|\.(?!\d)|&[lg]t;|(?!\b)(?=[A-Z][a-z])'
  - minify:
      minify_html: true
      minify_js: true
      minify_css: true
      htmlmin_opts:
        remove_comments: true
      cache_safe: true
  - git-revision-date-localized:
      enable_creation_date: true
      type: timeago
  - awesome-pages
  - include-markdown
  - macros:
      include_dir: docs/includes
  - mermaid2:
      arguments:
        theme: |
          ^(JSON.parse(__md_get("__palette").index == 1)) ?
          'dark' : 'light'

# Markdown Extensions
markdown_extensions:
  - abbr
  - admonition
  - attr_list
  - def_list
  - footnotes
  - md_in_html
  - toc:
      permalink: true
      title: On this page
  - pymdownx.arithmatex:
      generic: true
  - pymdownx.betterem:
      smart_enable: all
  - pymdownx.caret
  - pymdownx.details
  - pymdownx.emoji:
      emoji_generator: !!python/name:material.extensions.emoji.to_svg
      emoji_index: !!python/name:material.extensions.emoji.twemoji
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite
  - pymdownx.keys
  - pymdownx.magiclink:
      normalize_issue_symbols: true
      repo_url_shorthand: true
      user: malvavisc0
      repo: enhancedtoolkits
  - pymdownx.mark
  - pymdownx.smartsymbols
  - pymdownx.snippets:
      auto_append:
        - includes/abbreviations.md
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed:
      alternate_style: true
      combine_header_slug: true
      slugify: !!python/object/apply:pymdownx.slugs.slugify
        kwds:
          case: lower
  - pymdownx.tasklist:
      custom_checkbox: true
  - pymdownx.tilde

# Navigation
nav:
  - Home: index.md
  - Getting Started:
    - getting-started/index.md
    - Installation: getting-started/installation.md
    - Quick Start: getting-started/quick-start.md
    - Configuration: getting-started/configuration.md
    - Environment Variables: getting-started/environment.md
  - Core Toolkits:
    - toolkits/index.md
    - Reasoning Tools: toolkits/reasoning.md
    - Search Tools (SearxNG): toolkits/searxng.md
    - Thinking Tools: toolkits/thinking.md
    - Files Tools: toolkits/files.md
    - Finance Tools (YFinance): toolkits/finance.md
    - YouTube Tools: toolkits/youtube.md
    - Weather Tools: toolkits/weather.md
    - Downloader Tools: toolkits/downloader.md
  - Calculator Modules:
    - calculators/index.md
    - Arithmetic Calculator: calculators/arithmetic.md
    - Time Value Calculator: calculators/time-value.md
    - Investment Analysis: calculators/investment.md
    - Loan Calculator: calculators/loan.md
    - Bond Calculator: calculators/bond.md
    - Risk Metrics Calculator: calculators/risk.md
    - Depreciation Calculator: calculators/depreciation.md
    - Business Analysis: calculators/business.md
    - Utility Calculator: calculators/utility.md
  - Advanced Features:
    - advanced/index.md
    - Security & Validation: advanced/security.md
    - Error Handling: advanced/error-handling.md
    - Caching & Rate Limiting: advanced/performance.md
    - Session Management: advanced/sessions.md
    - StrictToolkit Base: advanced/strict-toolkit.md
  - API Reference:
    - api/index.md
    - Base Classes: api/base.md
    - Utilities: api/utils.md
    - Schemas: api/schemas.md
    - Error Classes: api/errors.md
  - Developer Guide:
    - developer/index.md
    - Contributing: developer/contributing.md
    - Testing: developer/testing.md
    - Deployment: developer/deployment.md
    - Release Process: developer/releases.md

# Extra CSS and JavaScript
extra_css:
  - assets/css/custom.css
  - assets/css/termynal.css

extra_javascript:
  - assets/js/custom.js
  - assets/js/termynal.js
  - https://polyfill.io/v3/polyfill.min.js?features=es6
  - https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js

# Extra configuration
extra:
  version:
    provider: mike
    default: latest
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/malvavisc0/enhancedtoolkits
      name: GitHub Repository
    - icon: fontawesome/brands/python
      link: https://pypi.org/project/enhancedtoolkits/
      name: PyPI Package
  analytics:
    provider: google
    property: !ENV GOOGLE_ANALYTICS_KEY
  consent:
    title: Cookie consent
    description: >- 
      We use cookies to recognize your repeated visits and preferences, as well
      as to measure the effectiveness of our documentation and whether users
      find what they're searching for. With your consent, you're helping us to
      make our documentation better.

# Validation
validation:
  omitted_files: warn
  absolute_links: warn
  unrecognized_links: warn

# Watch additional files
watch:
  - src/enhancedtoolkits
```

## Additional Files Needed

### 1. Custom CSS (`docs/assets/css/custom.css`)
```css
/* Custom styles for Enhanced Toolkits documentation */
:root {
  --md-primary-fg-color: #1976d2;
  --md-primary-fg-color--light: #42a5f5;
  --md-primary-fg-color--dark: #1565c0;
  --md-accent-fg-color: #4caf50;
}

/* Logo styling */
.md-header__button.md-logo img {
  height: 32px;
  width: auto;
}

/* Code block enhancements */
.highlight .filename {
  background: var(--md-code-bg-color);
  border-bottom: 1px solid var(--md-default-fg-color--lightest);
  color: var(--md-default-fg-color--light);
  font-size: 0.85em;
  padding: 0.5rem 1rem;
  margin: 0;
}

/* Toolkit cards */
.toolkit-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
  margin: 2rem 0;
}

.toolkit-card {
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 0.5rem;
  padding: 1.5rem;
  transition: box-shadow 0.2s;
}

.toolkit-card:hover {
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.toolkit-card h3 {
  margin-top: 0;
  color: var(--md-primary-fg-color);
}

/* Feature highlights */
.feature-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin: 2rem 0;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.feature-icon {
  color: var(--md-accent-fg-color);
  font-size: 1.5rem;
  margin-top: 0.25rem;
}

/* Installation badges */
.badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin: 1rem 0;
}

/* API documentation styling */
.api-method {
  border-left: 4px solid var(--md-primary-fg-color);
  padding-left: 1rem;
  margin: 1rem 0;
}

.api-method h4 {
  margin-top: 0;
  color: var(--md-primary-fg-color);
}

.parameter-table {
  margin: 1rem 0;
}

.parameter-table th {
  background: var(--md-default-fg-color--lightest);
}

/* Responsive adjustments */
@media screen and (max-width: 768px) {
  .toolkit-grid {
    grid-template-columns: 1fr;
  }
  
  .feature-list {
    grid-template-columns: 1fr;
  }
}
```

### 2. Custom JavaScript (`docs/assets/js/custom.js`)
```javascript
// Custom JavaScript for Enhanced Toolkits documentation

document.addEventListener('DOMContentLoaded', function() {
  // Add copy buttons to code blocks
  const codeBlocks = document.querySelectorAll('pre code');
  codeBlocks.forEach(function(block) {
    const button = document.createElement('button');
    button.className = 'md-clipboard md-icon';
    button.title = 'Copy to clipboard';
    button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z" /></svg>';
    
    button.addEventListener('click', function() {
      navigator.clipboard.writeText(block.textContent);
      button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z" /></svg>';
      setTimeout(function() {
        button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z" /></svg>';
      }, 2000);
    });
    
    block.parentNode.appendChild(button);
  });
  
  // Smooth scrolling for anchor links
  const anchorLinks = document.querySelectorAll('a[href^="#"]');
  anchorLinks.forEach(function(link) {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
});
```

### 3. Abbreviations (`docs/includes/abbreviations.md`)
```markdown
*[AI]: Artificial Intelligence
*[API]: Application Programming Interface
*[CLI]: Command Line Interface
*[HTTP]: HyperText Transfer Protocol
*[HTTPS]: HyperText Transfer Protocol Secure
*[JSON]: JavaScript Object Notation
*[NPV]: Net Present Value
*[IRR]: Internal Rate of Return
*[ROI]: Return on Investment
*[CAGR]: Compound Annual Growth Rate
*[YTM]: Yield to Maturity
*[ESG]: Environmental, Social, and Governance
*[TTL]: Time To Live
*[URL]: Uniform Resource Locator
*[UUID]: Universally Unique Identifier
*[CSV]: Comma-Separated Values
*[XML]: eXtensible Markup Language
*[YAML]: YAML Ain't Markup Language
*[PDF]: Portable Document Format
*[SEO]: Search Engine Optimization
```

This configuration provides a comprehensive, professional documentation site that showcases all the features of your Enhanced Toolkits library with excellent user experience and developer-friendly features.