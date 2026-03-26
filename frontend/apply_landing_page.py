import re

with open('src/views/Home.vue', 'r', encoding='utf-8') as f:
    text = f.read()

new_template = '''<template>
  <div class="landing-page">
    <header class="landing-header">
      <div class="nav-container">
        <div class="logo-container">
          <img src="/geopulse-logo.svg" alt="GeoPulse" class="nav-logo" />
          <span class="logo-text">GeoPulse</span>
        </div>
        <div class="nav-actions">
          <DarkModeSwitcher class="theme-button" />
          <div class="auth-actions" v-if="!isResolvingAuth">
            <template v-if="authStore.isAuthenticated">
              <Button label="Dashboard" as="router-link" to="/app/timeline" class="nav-btn-primary" size="small" />
              <Button icon="pi pi-sign-out" severity="secondary" text @click="handleSignOut" />
            </template>
            <template v-else>
              <Button v-if="isLoginAvailable" label="Sign In" icon="pi pi-sign-in" as="router-link" to="/login" severity="secondary" text class="nav-signin" />
            </template>
          </div>
        </div>
      </div>
    </header>

    <main class="landing-main">
      <section class="hero-section">
        <div class="hero-container">
          <div class="hero-content">
            <div class="hero-eyebrow">Self-hosted location timeline</div>
            <h1 class="hero-title" v-html="heroTitle"></h1>
            <p class="hero-subtitle" v-if="!isMobileViewport">GeoPulse turns raw GPS points into stays, trips, maps, and insights while your data stays under your control.</p>
            
            <div class="hero-ctas" v-if="!isResolvingAuth">
              <template v-if="!authStore.isAuthenticated">
                <Button v-if="isRegistrationAvailable" label="Start Your Journey" icon="pi pi-arrow-right" as="router-link" to="/register" size="large" class="cta-primary" />
                <Button v-else-if="isLoginAvailable" label="Sign In To Continue" icon="pi pi-sign-in" as="router-link" to="/login" size="large" class="cta-primary" />
              </template>
              <template v-else>
                <div class="welcome-back-box">
                  <p class="welcome-text">Welcome back! Continue exactly where you left off.</p>
                  <Button label="Continue to Dashboard" icon="pi pi-arrow-right" as="router-link" :to="continueDestination.path" size="large" class="cta-primary" />
                </div>
              </template>
            </div>
            <div v-else class="loading-auth">
               <i class="pi pi-spin pi-spinner"></i> Loading workspace...
            </div>
          </div>

          <div class="hero-visual">
            <div class="visual-showcase">
              <div class="orbit-ring ring-1"></div>
              <div class="orbit-ring ring-2"></div>
              <div class="orbit-ring ring-3"></div>
              <img src="/geopulse-logo.svg" alt="GeoPulse logo" class="massive-logo" />
              
              <div class="feature-chip chip-1"><div class="chip-icon"><i class="pi pi-send"></i></div><span>Live Tracking</span></div>
              <div class="feature-chip chip-2"><div class="chip-icon"><i class="pi pi-download"></i></div><span>Smart Import</span></div>
              <div class="feature-chip chip-3"><div class="chip-icon"><i class="pi pi-calendar"></i></div><span>Auto-Timeline</span></div>
              <div class="feature-chip chip-4"><div class="chip-icon"><i class="pi pi-chart-line"></i></div><span>Deep Insights</span></div>
              <div class="feature-chip chip-5"><div class="chip-icon"><i class="pi pi-images"></i></div><span>Immich Integration</span></div>
              <div class="feature-chip chip-6"><div class="chip-icon"><i class="pi pi-shield"></i></div><span>SSO & Roles</span></div>
            </div>
          </div>
        </div>
      </section>

      <section v-if="shouldShowQuickStats" class="quick-stats-section">
        <div class="content-wrapper">
          <div class="quick-stats-grid">
            <article class="quick-stat-tile quick-stat-latest">
              <div class="quick-stat-head">
                <span class="quick-stat-icon"><i class="pi pi-history"></i></span>
                <p class="quick-stat-label">Latest GPS update</p>
              </div>
              <p class="quick-stat-value">{{ latestGpsUpdateLabel }}</p>
            </article>
            <article class="quick-stat-tile quick-stat-distance">
              <div class="quick-stat-head">
                <span class="quick-stat-icon"><i class="pi pi-map-marker"></i></span>
                <p class="quick-stat-label">Distance today</p>
              </div>
              <p class="quick-stat-value">{{ distanceTodayLabel }}</p>
            </article>
            <article class="quick-stat-tile quick-stat-moving">
              <div class="quick-stat-head">
                <span class="quick-stat-icon"><i class="pi pi-send"></i></span>
                <p class="quick-stat-label">Time moving today</p>
              </div>
              <p class="quick-stat-value">{{ timeMovingTodayLabel }}</p>
            </article>
          </div>
        </div>
      </section>

      <section v-if="!isResolvingAuth && !authStore.isAuthenticated" class="features-section">
        <div class="content-wrapper">
          <div class="section-header">
            <h2>Core Capabilities</h2>
            <p>Built for self-hosted tracking: ingest data, analyze movement, and control your sharing entirely.</p>
          </div>

          <div class="feature-bento-grid">
            <Card v-for="feature in visibleFeatures" :key="feature.id" class="bento-card">
              <template #content>
                <div class="bento-icon">
                  <i :class="feature.icon"></i>
                </div>
                <h3>{{ feature.title }}</h3>
                <p>{{ feature.description }}</p>
              </template>
            </Card>
          </div>

          <Button
            v-if="!isDesktopViewport && !isMobileViewport && hasHiddenFeatures"
            :label="showAllFeatures ? 'Show fewer' : 'Show all capabilities'"
            :icon="showAllFeatures ? 'pi pi-angle-up' : 'pi pi-angle-down'"
            severity="secondary"
            outlined
            class="mobile-feature-toggle"
            @click="toggleFeatureVisibility"
          />
        </div>
      </section>
    </main>
    
    <footer class="landing-footer" v-if="!authStore.isAuthenticated">
      <div class="content-wrapper">
        <p>&copy; GeoPulse. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>'''

new_style = '''<style scoped>
.landing-page {
  --home-bg: var(--gp-surface-light, #f8fafc);
  --home-card-bg: var(--gp-surface-white, #ffffff);
  --home-text-primary: var(--gp-text-primary, #0f172a);
  --home-text-secondary: var(--gp-text-secondary, #475569);
  --home-border: var(--gp-border-light, #e2e8f0);
  --home-shadow: var(--gp-shadow-light, 0 8px 30px rgba(15, 23, 42, 0.04));
  --home-accent: var(--gp-primary, #0f766e);
  --home-accent-hover: var(--gp-primary-hover, #0d615a);
  --home-hero-gradient: linear-gradient(145deg, #f8fbff 0%, #edf3ff 52%, #e8f0ff 100%);
  --home-hero-glow: radial-gradient(ellipse at 80% 20%, rgba(37, 99, 235, 0.08) 0%, transparent 50%);
  
  min-height: 100vh;
  background: var(--home-bg);
  color: var(--home-text-primary);
  font-family: inherit;
  display: flex;
  flex-direction: column;
}

.landing-header { position: sticky; top: 0; z-index: 50; background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(12px); border-bottom: 1px solid var(--home-border); }

.nav-container, .content-wrapper { max-width: 1280px; margin: 0 auto; padding: 0 1.5rem; }
.nav-container { display: flex; justify-content: space-between; align-items: center; height: 4.5rem; }

.logo-container { display: flex; align-items: center; gap: 0.75rem; text-decoration: none; }
.nav-logo { height: 2rem; width: auto; }
.logo-text { font-size: 1.3rem; font-weight: 700; color: var(--home-text-primary); letter-spacing: -0.01em; }

.nav-actions { display: flex; align-items: center; gap: 1rem; }
.auth-actions { display: flex; align-items: center; gap: 0.5rem; }
.theme-button :deep(.p-button) { width: 2.2rem !important; height: 2.2rem !important; border-radius: 50% !important; border: 1px solid var(--home-border) !important; background: var(--home-card-bg) !important; color: var(--home-text-secondary) !important; }
.nav-btn-primary { border-radius: 99px !important; padding: 0.5rem 1.25rem !important; font-weight: 600 !important; background: var(--home-accent) !important; border-color: var(--home-accent) !important; }
.nav-signin { font-weight: 600 !important; color: var(--home-text-primary) !important; }

.landing-main { flex: 1; }

.hero-section { position: relative; padding: 4rem 1.5rem; background: var(--home-hero-gradient); overflow: hidden; border-bottom: 1px solid var(--home-border); }
.hero-section::before { content: ''; position: absolute; inset: 0; background: var(--home-hero-glow); z-index: 0; pointer-events: none; }

.hero-container { max-width: 1280px; margin: 0 auto; display: grid; grid-template-columns: 1fr; gap: 3rem; position: relative; z-index: 10; }
@media (min-width: 1024px) { .hero-container { grid-template-columns: 1fr 1fr; gap: 4rem; align-items: center; padding: 3rem 0; } }

.hero-content { display: flex; flex-direction: column; align-items: flex-start; }
.hero-eyebrow { display: inline-block; padding: 0.4rem 1rem; background: rgba(15, 118, 110, 0.1); color: var(--home-accent); border-radius: 9999px; font-size: 0.85rem; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 1.5rem; }
.hero-title { font-size: clamp(2.5rem, 5vw, 4rem); line-height: 1.1; font-weight: 800; letter-spacing: -0.03em; margin: 0 0 1.25rem 0; color: var(--home-text-primary); }
.hero-subtitle { font-size: clamp(1.1rem, 2vw, 1.25rem); line-height: 1.6; color: var(--home-text-secondary); margin: 0 0 2rem 0; max-width: 500px; }

.hero-ctas { display: flex; flex-direction: column; gap: 1rem; width: 100%; max-width: 320px; }
.cta-primary { padding: 1rem 1.5rem !important; font-size: 1.1rem !important; font-weight: 600 !important; border-radius: 0.75rem !important; background: linear-gradient(135deg, var(--home-accent) 0%, var(--home-accent-hover) 100%) !important; border: none !important; box-shadow: 0 4px 15px rgba(15, 118, 110, 0.3) !important; transition: all 0.2s ease !important; color: #fff !important; }
.cta-primary:hover { box-shadow: 0 6px 20px rgba(15, 118, 110, 0.4) !important; transform: translateY(-2px); }

.welcome-back-box { background: rgba(255,255,255,0.6); border: 1px solid var(--home-border); padding: 1.25rem; border-radius: 1rem; backdrop-filter: blur(8px); display: flex; flex-direction: column; gap: 0.75rem; }
.welcome-text { margin: 0; font-size: 0.95rem; color: var(--home-text-secondary); font-weight: 500; }
.loading-auth { font-size: 1.1rem; color: var(--home-text-secondary); display: flex; align-items: center; gap: 0.5rem; }

/* Right Panel Visuals */
.hero-visual { position: relative; min-height: 450px; display: flex; justify-content: center; align-items: center; }
.visual-showcase { position: relative; width: 100%; height: 100%; min-height: 450px; display: flex; align-items: center; justify-content: center; }
.massive-logo { width: 160px; height: 160px; z-index: 5; filter: drop-shadow(0 15px 30px rgba(15, 118, 110, 0.2)); position: relative; }
@media (min-width: 768px) { .massive-logo { width: 200px; height: 200px; } }

.orbit-ring { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); border-radius: 50%; border: 1px solid rgba(15, 118, 110, 0.12); z-index: 1; }
.ring-1 { width: 280px; height: 280px; } .ring-2 { width: 440px; height: 440px; border: 1px solid rgba(37, 99, 235, 0.08); } .ring-3 { width: 620px; height: 620px; border: 1px dashed rgba(14, 165, 233, 0.15); }

.feature-chip { position: absolute; display: flex; align-items: center; gap: 0.6rem; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(12px); padding: 0.4rem 1rem 0.4rem 0.4rem; border-radius: 999px; box-shadow: 0 4px 15px rgba(15, 23, 42, 0.08); border: 1px solid rgba(255, 255, 255, 1); font-weight: 600; font-size: 0.85rem; color: var(--home-text-primary); z-index: 10; white-space: nowrap; transition: transform 0.3s ease; }
.feature-chip:hover { transform: translateY(-3px) scale(1.02); }
.chip-icon { width: 2rem; height: 2rem; border-radius: 50%; background: rgba(15, 118, 110, 0.1); color: var(--home-accent); display: flex; align-items: center; justify-content: center; }
.chip-2 .chip-icon { background: rgba(37,99,235,0.1); color: #2563eb; } .chip-4 .chip-icon { background: rgba(147,51,234,0.1); color: #9333ea; } .chip-5 .chip-icon { background: rgba(234,88,12,0.1); color: #ea580c; } .chip-6 .chip-icon { background: rgba(225,29,72,0.1); color: #e11d48; }

@media (min-width: 1024px) {
  .chip-1 { top: 12%; left: 15%; } .chip-2 { top: 18%; right: -5%; } .chip-3 { bottom: 20%; left: -2%; } .chip-4 { bottom: 12%; right: 15%; } .chip-5 { top: 48%; left: 0%; } .chip-6 { bottom: 42%; right: -8%; }
}
@media (max-width: 1023px) {
  .hero-visual { min-height: 400px; overflow: hidden; padding-bottom: 2rem; } .massive-logo { position: absolute; }
  .chip-1 { top: 10%; left: 10%; } .chip-2 { top: 15%; right: 5%; } .chip-3 { bottom: 15%; left: 5%; } .chip-4 { bottom: 20%; right: 5%; } .chip-5 { top: 50%; left: -5%; } .chip-6 { bottom: 45%; right: -5%; }
  .orbit-ring { transform: translate(-50%, -50%) scale(0.85); }
}

/* Stats */
.quick-stats-section { padding: 3rem 0; background: var(--home-bg); }
.quick-stats-grid { display: grid; grid-template-columns: 1fr; gap: 1rem; }
@media (min-width: 768px) { .quick-stats-grid { grid-template-columns: repeat(3, 1fr); } }

.quick-stat-tile { background: var(--home-card-bg); border: 1px solid var(--home-border); border-radius: 1rem; padding: 1.5rem; display: flex; flex-direction: column; gap: 0.75rem; box-shadow: var(--home-shadow); }
.quick-stat-head { display: flex; align-items: center; gap: 0.75rem; }
.quick-stat-icon { width: 2.5rem; height: 2.5rem; border-radius: 0.5rem; background: rgba(15, 118, 110, 0.1); color: var(--home-accent); display: flex; align-items: center; justify-content: center; font-size: 1.2rem; }
.quick-stat-latest .quick-stat-icon { background: rgba(14, 165, 233, 0.1); color: #0ea5e9; }
.quick-stat-distance .quick-stat-icon { background: rgba(37, 99, 235, 0.1); color: #2563eb; }
.quick-stat-label { margin: 0; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--home-text-secondary); }
.quick-stat-value { margin: 0; font-size: 1.5rem; font-weight: 700; color: var(--home-text-primary); }

/* Features */
.features-section { padding: 5rem 0; background: var(--home-bg); }
.section-header { text-align: center; margin-bottom: 4rem; max-width: 700px; margin-left: auto; margin-right: auto; }
.section-header h2 { font-size: clamp(2rem, 4vw, 2.5rem); margin: 0 0 1rem 0; letter-spacing: -0.02em; color: var(--home-text-primary); }
.section-header p { font-size: 1.1rem; color: var(--home-text-secondary); margin: 0; line-height: 1.6; }

.feature-bento-grid { display: grid; grid-template-columns: 1fr; gap: 1.5rem; }
@media (min-width: 768px) { .feature-bento-grid { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 1024px) { .feature-bento-grid { grid-template-columns: repeat(3, 1fr); } }

.bento-card { background: var(--home-card-bg); border: 1px solid var(--home-border); border-radius: 1.25rem; box-shadow: var(--home-shadow); transition: transform 0.2s ease, box-shadow 0.2s ease; height: 100%; }
.bento-card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(15, 23, 42, 0.08); }
.bento-card :deep(.p-card-body) { padding: 2rem; height: 100%; display: flex; flex-direction: column; }
.bento-card :deep(.p-card-content) { padding: 0; flex: 1; display: flex; flex-direction: column; }

.bento-icon { width: 3rem; height: 3rem; border-radius: 0.75rem; background: linear-gradient(135deg, rgba(15, 118, 110, 0.15) 0%, rgba(14, 165, 233, 0.1) 100%); color: var(--home-accent); display: flex; align-items: center; justify-content: center; font-size: 1.4rem; margin-bottom: 1.5rem; border: 1px solid rgba(15, 118, 110, 0.2); }
.bento-card h3 { margin: 0 0 0.75rem 0; font-size: 1.2rem; font-weight: 700; color: var(--home-text-primary); }
.bento-card p { margin: 0; font-size: 0.95rem; line-height: 1.6; color: var(--home-text-secondary); flex: 1; }

.mobile-feature-toggle { margin-top: 2rem; width: 100%; }
.landing-footer { padding: 2rem 0; border-top: 1px solid var(--home-border); text-align: center; color: var(--home-text-secondary); font-size: 0.9rem; }

/* Dark Mode Overrides */
.p-dark .landing-page {
  --home-bg: #020617;
  --home-card-bg: #0f172a;
  --home-border: #1e293b;
  --home-text-primary: #f8fafc;
  --home-text-secondary: #94a3b8;
  --home-hero-gradient: linear-gradient(160deg, #020617 0%, #0a1128 50%, #03081a 100%);
  --home-hero-glow: radial-gradient(ellipse at 80% 20%, rgba(59, 130, 246, 0.15) 0%, transparent 60%);
}
.p-dark .landing-header { background: rgba(2, 6, 23, 0.85); border-bottom-color: rgba(255,255,255,0.05); }
.p-dark .feature-chip { background: rgba(15, 23, 42, 0.85); border-color: #334155; }
.p-dark .bento-card, .p-dark .quick-stat-tile, .p-dark .welcome-back-box { background: rgba(15, 23, 42, 0.6); border-color: rgba(255,255,255,0.08); }
.p-dark .welcome-back-box { background: rgba(30, 41, 59, 0.5); }
.p-dark .orbit-ring { border-color: rgba(255,255,255,0.05); }
</style>'''

template_pattern = re.compile(r'<template>.*?</template>', re.DOTALL)
style_pattern = re.compile(r'<style scoped>.*?</style>', re.DOTALL)

# Use a function for replacement to avoid escape sequence issues
text = template_pattern.sub(lambda m: new_template, text)
text = style_pattern.sub(lambda m: new_style, text)

with open('src/views/Home.vue', 'w', encoding='utf-8') as f:
    f.write(text)
