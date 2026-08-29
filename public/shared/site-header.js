(() => {
  const script = document.currentScript;
  if (!script) return;

  const faviconUrl = new URL("./favicon.svg", script.src).href;
  const faviconLinks = document.querySelectorAll('link[rel~="icon"]');
  if (faviconLinks.length) {
    faviconLinks.forEach((link) => {
      link.href = faviconUrl;
      link.type = "image/svg+xml";
    });
  } else {
    const favicon = document.createElement("link");
    favicon.rel = "icon";
    favicon.type = "image/svg+xml";
    favicon.href = faviconUrl;
    document.head.append(favicon);
  }

  const gaMeasurementId = "G-FJMHVLKN37";
  if (!window.__dennoGaLoaded) {
    window.__dennoGaLoaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function gtag() { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("config", gaMeasurementId);

    const gaScript = document.createElement("script");
    gaScript.async = true;
    gaScript.src = `https://www.googletagmanager.com/gtag/js?id=${gaMeasurementId}`;
    document.head.append(gaScript);
  }

  if (document.querySelector(".denno-site-header")) return;

  const siteRoot = new URL("../", script.src);
  const pageUrl = new URL(window.location.href);
  const rootPath = siteRoot.pathname.replace(/\/+$/, "");
  const relativePath = decodeURIComponent(pageUrl.pathname.slice(rootPath.length)).replace(/^\/+/, "");
  const section = relativePath.split("/")[0];

  const links = [
    { key: "hunterdata", label: "神眼DB", path: "hunterdata/" },
    { key: "huntermizumi", label: "性格念診断", path: "huntermizumi/" },
    { key: "hunterkeisai", label: "WJ掲載号", path: "hunterkeisai/" },
    { key: "huntermeigen", label: "俺名台詞", path: "huntermeigen/" },
    { key: "coming-soon", label: "DDクイズ", path: "#coming-soon" },
  ];

  const header = document.createElement("header");
  header.className = "denno-site-header";
  header.innerHTML = `
    <div class="denno-header-inner">
      <a class="denno-brand" href="${new URL("./", siteRoot).href}" aria-label="電脳ハンター協会 トップ">
        <span class="denno-brand-mark" aria-hidden="true">H×H</span>
        <span class="denno-brand-copy">
          <span class="denno-brand-title">電脳ハンター協会</span>
          <span class="denno-brand-subtitle">HUNTER×HUNTER FAN SITE</span>
        </span>
      </a>
      <nav class="denno-global-nav" aria-label="主要コンテンツ">
        ${links.map((link) => {
          const active = link.key === section ? ' aria-current="page"' : "";
          return `<a href="${new URL(link.path, siteRoot).href}"${active}>${link.label}</a>`;
        }).join("")}
      </nav>
    </div>`;

  const legacyHeader = document.querySelector("body > header.site-header");
  document.body.classList.add("denno-has-shared-header");
  if (legacyHeader) document.body.classList.add("denno-hide-legacy-header");
  document.body.prepend(header);

  const syncHeaderHeight = () => {
    document.documentElement.style.setProperty("--denno-header-height", `${header.offsetHeight}px`);
  };
  syncHeaderHeight();
  if ("ResizeObserver" in window) new ResizeObserver(syncHeaderHeight).observe(header);
  else window.addEventListener("resize", syncHeaderHeight, { passive: true });
})();
