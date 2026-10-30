/**
 * The Apex Workflows Lab - Privacy-Centric Telemetry & Outbound Analytics
 * Zero cookies, zero third-party pixels, zero personal data collection.
 * Tracks reading engagement (scroll depth milestones) and Amazon affiliate CTA conversions.
 */
(function() {
    'use strict';

    const SESSION_ID = 'apex_' + Date.now().toString(36) + '_' + Math.random().toString(36).substring(2, 8);
    const PAGE_PATH = window.location.pathname;

    // 1. Outbound Amazon Affiliate Click Tracking
    document.addEventListener('click', function(e) {
        const link = e.target.closest('a');
        if (!link) return;

        const href = link.getAttribute('href') || '';
        if (href.includes('amazon.com') && href.includes('tag=')) {
            const asinMatch = href.match(/\/dp\/([A-Z0-9]{10})/i);
            const asin = asinMatch ? asinMatch[1] : 'UNKNOWN_ASIN';
            const clickPayload = {
                event: 'amazon_affiliate_click',
                asin: asin,
                url: href,
                page: PAGE_PATH,
                session_id: SESSION_ID,
                timestamp: new Date().toISOString()
            };

            // Local cache for auditing
            try {
                const logs = JSON.parse(localStorage.getItem('apex_conversion_logs') || '[]');
                logs.push(clickPayload);
                if (logs.length > 50) logs.shift();
                localStorage.setItem('apex_conversion_logs', JSON.stringify(logs));
            } catch (err) {}

            window.dispatchEvent(new CustomEvent('apex:conversion', { detail: clickPayload }));
        }
    });

    // 2. Reading Engagement (Scroll Milestones: 25%, 50%, 75%, 100%)
    const milestones = [25, 50, 75, 100];
    const loggedMilestones = new Set();

    function checkScrollDepth() {
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        if (docHeight <= 0) return;
        const currentPct = Math.round((window.scrollY / docHeight) * 100);

        milestones.forEach(function(m) {
            if (currentPct >= m && !loggedMilestones.has(m)) {
                loggedMilestones.add(m);
                const engagementPayload = {
                    event: 'scroll_depth_milestone',
                    depth_pct: m,
                    page: PAGE_PATH,
                    session_id: SESSION_ID,
                    timestamp: new Date().toISOString()
                };
                try {
                    const scrollLogs = JSON.parse(localStorage.getItem('apex_scroll_logs') || '[]');
                    scrollLogs.push(engagementPayload);
                    if (scrollLogs.length > 50) scrollLogs.shift();
                    localStorage.setItem('apex_scroll_logs', JSON.stringify(scrollLogs));
                } catch (err) {}
            }
        });
    }

    window.addEventListener('scroll', checkScrollDepth, { passive: true });
})();

