/**
 * The Apex Workflows Lab - Enterprise Telemetry & Conversion Analytics v2.0
 * Pure client-side, zero cookies, zero third-party tracking pixels, GDPR & CCPA compliant.
 * Captures referral intelligence (Reddit, Twitter/X, Search), reading dwell time,
 * interactive calculator anthropometrics, and outbound Amazon affiliate conversions.
 */
(function() {
    'use strict';

    // 1. Session & Referrer Acquisition Engine
    const SESSION_ID = 'apex_' + Date.now().toString(36) + '_' + Math.random().toString(36).substring(2, 7);
    const PAGE_PATH = window.location.pathname;
    const PAGE_TITLE = document.title;
    const SESSION_START = Date.now();

    // Parse URL params for UTM campaigns
    const urlParams = new URLSearchParams(window.location.search);
    const utmSource = urlParams.get('utm_source') || '';
    const utmMedium = urlParams.get('utm_medium') || '';
    const utmCampaign = urlParams.get('utm_campaign') || '';

    // Classify Referrer
    function getReferrerCategory() {
        if (utmSource.toLowerCase().includes('reddit')) return 'Reddit';
        if (utmSource.toLowerCase().includes('twitter') || utmSource.toLowerCase().includes('x')) return 'Twitter / X';
        
        const ref = (document.referrer || '').toLowerCase();
        if (!ref) return 'Direct / Bookmark';
        if (ref.includes('reddit.com') || ref.includes('redd.it')) return 'Reddit';
        if (ref.includes('t.co') || ref.includes('twitter.com') || ref.includes('x.com')) return 'Twitter / X';
        if (ref.includes('google.')) return 'Google Search';
        if (ref.includes('bing.')) return 'Bing Search';
        if (ref.includes('duckduckgo.')) return 'DuckDuckGo';
        if (ref.includes('linkedin.')) return 'LinkedIn';
        if (ref.includes('theapexworkflows.com')) return 'Internal Navigation';
        try {
            const host = new URL(ref).hostname;
            return host.replace('www.', '');
        } catch(e) {
            return 'Other External';
        }
    }

    const REFERRER_CATEGORY = getReferrerCategory();
    const REFERRER_RAW = document.referrer || '(Direct / None)';

    // Storage Keys
    const KEY_EVENTS = 'apex_telemetry_events';
    const KEY_METRICS = 'apex_telemetry_metrics';

    function getStoredMetrics() {
        try {
            return JSON.parse(localStorage.getItem(KEY_METRICS) || '{}');
        } catch (e) {
            return {};
        }
    }

    function saveStoredMetrics(metrics) {
        try {
            localStorage.setItem(KEY_METRICS, JSON.stringify(metrics));
        } catch (e) {}
    }

    function logTelemetryEvent(eventType, details) {
        const payload = {
            event_id: 'evt_' + Math.random().toString(36).substring(2, 9),
            type: eventType,
            timestamp: new Date().toISOString(),
            session_id: SESSION_ID,
            page: PAGE_PATH,
            referrer: REFERRER_CATEGORY,
            referrer_raw: REFERRER_RAW,
            utm: { source: utmSource, medium: utmMedium, campaign: utmCampaign },
            details: details || {}
        };

        // 1. Store in event log
        try {
            const events = JSON.parse(localStorage.getItem(KEY_EVENTS) || '[]');
            events.push(payload);
            if (events.length > 200) events.shift();
            localStorage.setItem(KEY_EVENTS, JSON.stringify(events));
        } catch (e) {}

        // 2. Update aggregate metrics
        try {
            const m = getStoredMetrics();
            m.total_page_views = (m.total_page_views || 0) + 1;
            m.referrers = m.referrers || {};
            m.referrers[REFERRER_CATEGORY] = (m.referrers[REFERRER_CATEGORY] || 0) + 1;

            if (eventType === 'amazon_affiliate_click') {
                m.total_amazon_clicks = (m.total_amazon_clicks || 0) + 1;
                m.products = m.products || {};
                const asin = details.asin || 'GENERAL';
                m.products[asin] = (m.products[asin] || 0) + 1;
            }

            if (eventType === 'calculator_calculate') {
                m.calculator_runs = (m.calculator_runs || 0) + 1;
            }

            saveStoredMetrics(m);
        } catch (e) {}

        // 3. Dispatch DOM event for reactive UI
        try {
            window.dispatchEvent(new CustomEvent('apex:telemetry', { detail: payload }));
        } catch (e) {}
    }

    // Log Page View initially
    logTelemetryEvent('page_view', { title: PAGE_TITLE });

    // 2. Outbound Amazon Affiliate CTA Tracking
    document.addEventListener('click', function(e) {
        const link = e.target.closest('a');
        if (!link) return;

        const href = link.getAttribute('href') || '';
        if (href.includes('amazon.com') && href.includes('tag=apexworkflows-20')) {
            const asinMatch = href.match(/\/dp\/([A-Z0-9]{10})/i);
            const queryMatch = href.match(/[?&]k=([^&]+)/i);
            const itemIdentifier = asinMatch ? asinMatch[1] : (queryMatch ? decodeURIComponent(queryMatch[1]).replace(/\+/g, ' ') : 'FEATURED_PRODUCT');
            const linkText = (link.innerText || link.getAttribute('aria-label') || 'CTA Link').trim().substring(0, 50);
            const dwellSec = Math.round((Date.now() - SESSION_START) / 1000);

            logTelemetryEvent('amazon_affiliate_click', {
                asin: itemIdentifier,
                url: href,
                link_text: linkText,
                dwell_seconds: dwellSec
            });
        }
    });

    // 3. Reading Engagement (Scroll Milestones: 25%, 50%, 75%, 100%)
    const milestones = [25, 50, 75, 100];
    const loggedMilestones = new Set();

    function checkScrollDepth() {
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        if (docHeight <= 0) return;
        const currentPct = Math.round((window.scrollY / docHeight) * 100);

        milestones.forEach(function(m) {
            if (currentPct >= m && !loggedMilestones.has(m)) {
                loggedMilestones.add(m);
                logTelemetryEvent('scroll_depth_milestone', {
                    depth_pct: m,
                    dwell_seconds: Math.round((Date.now() - SESSION_START) / 1000)
                });
            }
        });
    }
    window.addEventListener('scroll', checkScrollDepth, { passive: true });

    // 4. Reading Dwell Time Milestones (15s, 30s, 60s, 120s, 300s)
    const dwellCheckpoints = [15, 30, 60, 120, 300];
    dwellCheckpoints.forEach(function(sec) {
        setTimeout(function() {
            if (!document.hidden) {
                logTelemetryEvent('dwell_time_milestone', { seconds: sec });
            }
        }, sec * 1000);
    });

    // 5. Expose Global ApexTelemetry Controller for Interactive Tools (Calculator)
    window.ApexTelemetry = {
        log: logTelemetryEvent,
        getSessionId: function() { return SESSION_ID; },
        getReferrerCategory: function() { return REFERRER_CATEGORY; },
        getStoredMetrics: getStoredMetrics,
        getStoredEvents: function() {
            try {
                return JSON.parse(localStorage.getItem(KEY_EVENTS) || '[]');
            } catch(e) {
                return [];
            }
        },
        clearData: function() {
            localStorage.removeItem(KEY_EVENTS);
            localStorage.removeItem(KEY_METRICS);
        }
    };
})();
