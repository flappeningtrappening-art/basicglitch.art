/**
 * BASICGLITCH DEEP LORE TERMINAL
 * ==========================================
 * Interactive forensic interface for ARG.
 * ==========================================
 */

const LORE_VAULT = {
    "SIGNAL_77": "https://basicglitch.art/assets/images/raw/exclusive_starbot_blueprint.webp",
    "DECAY_0": "https://basicglitch.art/assets/images/raw/decay_process_highres.webp",
    "FOUNDRY_ROOT": "https://basicglitch.art/assets/images/raw/mainframe_access_unlocked.webp"
};

function openTerminal() {
    const input = prompt("ENTER_FORENSIC_FRAGMENT:");
    
    if (!input) return;

    const fragment = input.toUpperCase().trim();

    if (LORE_VAULT[fragment]) {
        alert("ACCESS GRANTED. DECRYPTING DATA STREAM...");
        window.open(LORE_VAULT[fragment], '_blank');
    } else {
        alert("ERROR: INVALID SIGNAL. ACCESS DENIED.");
        console.error("Forensic Mismatch detected for fragment: " + fragment);
    }
}

console.log("Deep Lore Terminal V1.0.4 Initialized. Awaiting forensic signal...");
