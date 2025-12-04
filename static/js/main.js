document.addEventListener("DOMContentLoaded", function () {
    console.log("Vasantha Heights site loaded.");

    const openBtn = document.getElementById("vh-contact-open");
    const closeBtn = document.getElementById("vh-contact-close");
    const drawer = document.getElementById("vh-contact-drawer");
    const overlay = document.getElementById("vh-contact-overlay");

    function openDrawer() {
        if (!drawer || !overlay) return;
        drawer.classList.add("vh-contact-drawer-open");
        overlay.classList.add("vh-contact-overlay-visible");
    }

    function closeDrawer() {
        if (!drawer || !overlay) return;
        drawer.classList.remove("vh-contact-drawer-open");
        overlay.classList.remove("vh-contact-overlay-visible");
    }

    if (openBtn) openBtn.addEventListener("click", openDrawer);
    if (closeBtn) closeBtn.addEventListener("click", closeDrawer);
    if (overlay) overlay.addEventListener("click", closeDrawer);
});
