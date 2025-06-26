// Custom JavaScript for Enhanced Toolkits documentation

document.addEventListener('DOMContentLoaded', function() {
  // Smooth scrolling for anchor links
  const anchorLinks = document.querySelectorAll('a[href^="#"]');
  anchorLinks.forEach(function(link) {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ 
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // Enhanced code block functionality
  const codeBlocks = document.querySelectorAll('pre code');
  codeBlocks.forEach(function(block) {
    // Add language label if available
    const language = block.className.match(/language-(\w+)/);
    if (language) {
      const label = document.createElement('div');
      label.className = 'code-language-label';
      label.textContent = language[1].toUpperCase();
      block.parentNode.insertBefore(label, block);
    }
  });

  // Add copy success feedback
  document.addEventListener('click', function(e) {
    if (e.target.closest('.md-clipboard')) {
      const button = e.target.closest('.md-clipboard');
      const originalTitle = button.title;
      button.title = 'Copied!';
      setTimeout(function() {
        button.title = originalTitle;
      }, 2000);
    }
  });

  // Enhance navigation experience
  const navLinks = document.querySelectorAll('.md-nav__link');
  navLinks.forEach(function(link) {
    link.addEventListener('click', function() {
      // Add loading state for navigation
      this.style.opacity = '0.7';
      setTimeout(() => {
        this.style.opacity = '1';
      }, 300);
    });
  });

  // Add keyboard shortcuts
  document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      const searchInput = document.querySelector('.md-search__input');
      if (searchInput) {
        searchInput.focus();
      }
    }
    
    // Escape to close search
    if (e.key === 'Escape') {
      const searchInput = document.querySelector('.md-search__input');
      if (searchInput && document.activeElement === searchInput) {
        searchInput.blur();
      }
    }
  });

  // Add scroll progress indicator
  function updateScrollProgress() {
    const scrollTop = window.pageYOffset;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const scrollPercent = (scrollTop / docHeight) * 100;
    
    let progressBar = document.querySelector('.scroll-progress');
    if (!progressBar) {
      progressBar = document.createElement('div');
      progressBar.className = 'scroll-progress';
      progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: ${scrollPercent}%;
        height: 3px;
        background: var(--md-primary-fg-color);
        z-index: 1000;
        transition: width 0.1s ease;
      `;
      document.body.appendChild(progressBar);
    } else {
      progressBar.style.width = scrollPercent + '%';
    }
  }

  // Throttled scroll handler
  let scrollTimeout;
  window.addEventListener('scroll', function() {
    if (scrollTimeout) {
      clearTimeout(scrollTimeout);
    }
    scrollTimeout = setTimeout(updateScrollProgress, 10);
  });

  // Initialize scroll progress
  updateScrollProgress();

  // Add external link indicators
  const externalLinks = document.querySelectorAll('a[href^="http"]:not([href*="' + window.location.hostname + '"])');
  externalLinks.forEach(function(link) {
    link.setAttribute('target', '_blank');
    link.setAttribute('rel', 'noopener noreferrer');
    
    // Add external link icon
    const icon = document.createElement('span');
    icon.innerHTML = ' ↗';
    icon.style.fontSize = '0.8em';
    icon.style.opacity = '0.7';
    link.appendChild(icon);
  });

  // Enhance table responsiveness
  const tables = document.querySelectorAll('table');
  tables.forEach(function(table) {
    const wrapper = document.createElement('div');
    wrapper.className = 'table-wrapper';
    wrapper.style.cssText = 'overflow-x: auto; margin: 1rem 0;';
    table.parentNode.insertBefore(wrapper, table);
    wrapper.appendChild(table);
  });

  // Add print-friendly styles
  const printStyles = document.createElement('style');
  printStyles.textContent = `
    @media print {
      .md-header, .md-footer, .md-sidebar { display: none !important; }
      .md-content { margin: 0 !important; }
      .scroll-progress { display: none !important; }
    }
  `;
  document.head.appendChild(printStyles);
});

// Utility functions
window.EnhancedToolkitsUtils = {
  // Copy text to clipboard
  copyToClipboard: function(text) {
    if (navigator.clipboard) {
      return navigator.clipboard.writeText(text);
    } else {
      // Fallback for older browsers
      const textArea = document.createElement('textarea');
      textArea.value = text;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
      return Promise.resolve();
    }
  },

  // Highlight code syntax
  highlightCode: function(element) {
    if (window.hljs) {
      window.hljs.highlightElement(element);
    }
  },

  // Scroll to element with offset
  scrollToElement: function(element, offset = 80) {
    const elementPosition = element.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - offset;
    
    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    });
  }
};