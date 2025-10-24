// ==========================================
// HOSPITAL MANAGEMENT SYSTEM - DJANGO ADMIN ENHANCEMENTS
// Modern, Interactive JavaScript for Enhanced UX
// ==========================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('🏥 Hospital Management Admin - Enhanced Mode Activated');

    // ==========================================
    // PAGE LOAD ANIMATIONS
    // ==========================================

    // Add smooth page load animation
    const adminContent = document.querySelector('#content, .content-wrapper');
    if (adminContent) {
        adminContent.style.opacity = '0';
        adminContent.style.transform = 'translateY(20px)';
        adminContent.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';

        setTimeout(() => {
            adminContent.style.opacity = '1';
            adminContent.style.transform = 'translateY(0)';
        }, 100);
    }

    // ==========================================
    // ENHANCED STATUS BADGES
    // ==========================================

    // Enhanced status badges with animations
    const statusBadges = document.querySelectorAll('.status-badge, .status_badge');
    statusBadges.forEach((badge, index) => {
        // Add staggered animation
        badge.style.opacity = '0';
        badge.style.transform = 'scale(0.8)';

        setTimeout(() => {
            badge.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
            badge.style.opacity = '1';
            badge.style.transform = 'scale(1)';
        }, index * 50 + 200);

        // Add hover effects
        badge.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1) translateY(-2px)';
            this.style.boxShadow = '0 4px 8px rgba(0,0,0,0.15)';
        });

        badge.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1) translateY(0)';
            this.style.boxShadow = 'none';
        });
    });

    // ==========================================
    // INTERACTIVE ACTION BUTTONS
    // ==========================================

    // Enhanced action buttons with ripple effects
    const actionButtons = document.querySelectorAll('.action-btn, .button, input[type="submit"]');
    actionButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Create ripple effect
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255,255,255,0.3)';
            ripple.style.pointerEvents = 'none';
            ripple.style.animation = 'ripple 0.6s linear';

            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);

            setTimeout(() => {
                ripple.remove();
            }, 600);

            // Add click feedback
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    });

    // ==========================================
    // ENHANCED DELETE CONFIRMATIONS
    // ==========================================

    // Enhanced delete confirmations with better UX
    const deleteButtons = document.querySelectorAll('a[href*="delete"], .deletelink');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();

            const tokenNumber = this.closest('tr')?.querySelector('.token-number, .field-token_number')?.textContent?.trim();
            const patientName = this.closest('tr')?.querySelector('.patient-link')?.textContent?.trim();

            const itemName = tokenNumber ? `Token ${tokenNumber}` : (patientName ? `Patient ${patientName}` : 'this item');

            // Create custom confirmation modal
            const modal = document.createElement('div');
            modal.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.5);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10000;
                backdrop-filter: blur(2px);
            `;

            const modalContent = document.createElement('div');
            modalContent.style.cssText = `
                background: white;
                padding: 32px;
                border-radius: 16px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.15);
                max-width: 400px;
                width: 90%;
                text-align: center;
                animation: modalSlideIn 0.3s ease;
            `;

            modalContent.innerHTML = `
                <div style="font-size: 48px; color: #ef4444; margin-bottom: 16px;">⚠️</div>
                <h3 style="margin: 0 0 16px 0; color: #1f2937; font-weight: 600;">Confirm Deletion</h3>
                <p style="margin: 0 0 24px 0; color: #6b7280; line-height: 1.6;">
                    Are you sure you want to delete <strong>${itemName}</strong>?<br>
                    This action cannot be undone.
                </p>
                <div style="display: flex; gap: 12px; justify-content: center;">
                    <button id="confirmDelete" style="
                        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
                        color: white;
                        border: none;
                        padding: 12px 24px;
                        border-radius: 8px;
                        font-weight: 600;
                        cursor: pointer;
                        transition: all 0.2s ease;
                    ">Delete</button>
                    <button id="cancelDelete" style="
                        background: #f3f4f6;
                        color: #374151;
                        border: 1px solid #d1d5db;
                        padding: 12px 24px;
                        border-radius: 8px;
                        font-weight: 600;
                        cursor: pointer;
                        transition: all 0.2s ease;
                    ">Cancel</button>
                </div>
            `;

            modal.appendChild(modalContent);
            document.body.appendChild(modal);

            // Add modal slide-in animation
            const style = document.createElement('style');
            style.textContent = `
                @keyframes modalSlideIn {
                    from { transform: scale(0.9) translateY(-20px); opacity: 0; }
                    to { transform: scale(1) translateY(0); opacity: 1; }
                }
                @keyframes ripple {
                    to { transform: scale(4); opacity: 0; }
                }
            `;
            document.head.appendChild(style);

            // Handle modal actions
            document.getElementById('confirmDelete').onclick = () => {
                modal.remove();
                window.location.href = button.href;
            };

            document.getElementById('cancelDelete').onclick = () => {
                modal.remove();
            };

            modal.onclick = (e) => {
                if (e.target === modal) {
                    modal.remove();
                }
            };
        });
    });

    // ==========================================
    // AUTO-REFRESH FOR QUEUE MANAGEMENT
    // ==========================================

    // Smart auto-refresh for queue tokens page
    if (window.location.pathname.includes('/admin/hospital/queuetoken/')) {
        let refreshInterval;

        const startAutoRefresh = () => {
            refreshInterval = setInterval(() => {
                // Check if any forms are being edited
                const forms = document.querySelectorAll('form');
                const hasUnsavedChanges = Array.from(forms).some(form =>
                    form.classList.contains('has-unsaved-changes') ||
                    form.querySelectorAll('input:focus, select:focus, textarea:focus').length > 0
                );

                if (!hasUnsavedChanges) {
                    // Add loading indicator
                    const refreshButton = document.querySelector('.fa-sync-alt')?.parentElement;
                    if (refreshButton) {
                        refreshButton.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i> Refreshing...';
                    }

                    window.location.reload();
                }
            }, 30000); // 30 seconds
        };

        const stopAutoRefresh = () => {
            if (refreshInterval) {
                clearInterval(refreshInterval);
            }
        };

        // Start auto-refresh
        startAutoRefresh();

        // Pause on user interaction
        ['mousedown', 'keydown', 'scroll'].forEach(event => {
            document.addEventListener(event, () => {
                stopAutoRefresh();
                setTimeout(startAutoRefresh, 5000); // Resume after 5 seconds of inactivity
            }, { once: true });
        });
    }

    // ==========================================
    // KEYBOARD SHORTCUTS
    // ==========================================

    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + R for refresh
        if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
            e.preventDefault();
            window.location.reload();
        }

        // Escape key to go back
        if (e.key === 'Escape') {
            const breadcrumbLinks = document.querySelectorAll('.breadcrumb a');
            if (breadcrumbLinks.length > 0) {
                window.location.href = breadcrumbLinks[0].href;
            }
        }

        // Ctrl/Cmd + S to save (if form is present)
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            const saveButton = document.querySelector('input[type="submit"][value*="Save"], .button.default');
            if (saveButton) {
                saveButton.click();
            }
        }
    });

    // ==========================================
    // ENHANCED SEARCH FUNCTIONALITY
    // ==========================================

    // Enhanced search with visual feedback
    const searchInputs = document.querySelectorAll('input[type="search"], input[name="q"], #searchbar');
    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            const query = this.value;

            if (query.length > 2) {
                // Active search styling
                this.style.borderColor = '#3b82f6';
                this.style.boxShadow = '0 0 0 3px rgba(59, 130, 246, 0.1)';
                this.style.background = 'linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%)';
            } else if (query.length === 0) {
                // Reset styling
                this.style.borderColor = '';
                this.style.boxShadow = '';
                this.style.background = '';
            } else {
                // Searching state
                this.style.borderColor = '#f59e0b';
                this.style.boxShadow = '0 0 0 3px rgba(245, 158, 11, 0.1)';
                this.style.background = 'linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%)';
            }
        });

        // Add search icon animation
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
            this.parentElement.style.transition = 'transform 0.2s ease';
        });

        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
        });
    });

    // ==========================================
    // RESPONSIVE TABLE ENHANCEMENTS
    // ==========================================

    // Add mobile-friendly table scrolling
    const tables = document.querySelectorAll('#result_list, .results table');
    tables.forEach(table => {
        if (window.innerWidth <= 768) {
            table.style.overflowX = 'auto';
            table.style.display = 'block';
            table.style.whiteSpace = 'nowrap';
        }
    });

    // ==========================================
    // NOTIFICATION ENHANCEMENTS
    // ==========================================

    // Enhanced Django messages with animations
    const messages = document.querySelectorAll('.message');
    messages.forEach((message, index) => {
        message.style.opacity = '0';
        message.style.transform = 'translateY(-10px)';

        setTimeout(() => {
            message.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
            message.style.opacity = '1';
            message.style.transform = 'translateY(0)';
        }, index * 100 + 500);

        // Auto-hide after 5 seconds
        setTimeout(() => {
            message.style.opacity = '0';
            message.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                if (message.parentNode) {
                    message.remove();
                }
            }, 400);
        }, 5000);
    });

    // ==========================================
    // PERFORMANCE MONITORING
    // ==========================================

    // Log performance metrics
    window.addEventListener('load', function() {
        setTimeout(() => {
            const perfData = performance.getEntriesByType('navigation')[0];
            if (perfData) {
                console.log(`⚡ Page loaded in ${Math.round(perfData.loadEventEnd - perfData.fetchStart)}ms`);
            }
        }, 0);
    });

    console.log('✅ Hospital Management Admin - All enhancements loaded');
});
