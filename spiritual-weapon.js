/* The two spectral fists are one spell and share one bonus action. */
(() => {
  'use strict';
  const {makeAttackRoll, askHit, roll, addLog, ribbon, commitAttack} = ZephyrNative;
  const bridge = window.__CompanionBridge;
  const state = () => bridge.read();
  const byId = id => document.getElementById(id);
  const card = byId('spiritualWeaponCard');
  const strike = byId('spiritualStrike');
  const move = byId('spiritualMove');
  const dismiss = byId('spiritualDismiss');
  const invoke = document.querySelector('[data-name="Arme spirituelle"]');
  const diceCount = level => 1 + Math.floor((level - 2) / 2);
  let running = false;

  function effect() {
    const s = state();
    if (!(s.spiritualUntil > s.turn)) return null;
    if (s.spiritualCombatId && RPGConnect.getStatus().controlled &&
        RPGHealth.getContext().combatId !== s.spiritualCombatId) return null;
    return {level: s.spiritualLevel || 2, remaining: Math.min(10, s.spiritualUntil - s.turn)};
  }

  function usage() {
    const s = state();
    return s.spiritualBonus?.turn === s.turn ? s.spiritualBonus : null;
  }

  function draw() {
    const active = effect();
    const s = state();
    const used = usage();
    const busy = running || !!s.rpgZephyrAttack || !!s.rpgSpiritualAttack;
    card.hidden = !active;
    invoke.disabled = busy || !!s.eco.b || !!s.leveledAction || RPGCombatEffectsClient.busy();
    const spellStatus = byId('spiritualSpellState');
    spellStatus.textContent = active ? 'Poings actifs · ' + active.remaining + '/10 tours' : '';
    spellStatus.hidden = !active;
    if (!active) return;
    byId('spiritualDamage').textContent = diceCount(active.level) + 'd8+4';
    byId('spiritualCastLevel').textContent = 'Niv. ' + active.level;
    byId('spiritualDuration').value = active.remaining;
    byId('spiritualTurns').textContent = active.remaining + '/10 tours';
    strike.disabled = busy || !!used?.struck || (s.eco.b && !used);
    move.disabled = busy || !!used?.moved || !!used?.initial || (s.eco.b && !used);
    move.textContent = used?.moved ? 'Déplacés · 6 m max.' : 'Déplacer (6 m)';
    dismiss.disabled = busy;
  }

  function activate(level, parent = {}) {
    const s = state();
    s.spiritualLevel = level;
    s.spiritualUntil = s.turn + 10;
    s.spiritualCombatId = parent.combatId || null;
    s.spiritualBonus = {turn: s.turn, initial: true, actionId: parent.actionId, before: parent.before};
    bridge.healthRefresh();
    draw();
  }

  function moveWeapon() {
    if (move.disabled || !effect()) return;
    const s = state();
    const used = usage() || {turn: s.turn};
    s.eco.b = true;
    used.moved = true;
    s.spiritualBonus = used;
    addLog('Poings du Serment', 'Déplacement de l’arme jusqu’à 6 m', 'spell');
    draw();
  }

  function dismissWeapon() {
    if (dismiss.disabled || !effect()) return;
    state().spiritualUntil = 0;
    addLog('Poings du Serment', 'Arme spirituelle dissipée', 'spell');
    draw();
  }

  async function attack() {
    if (running) return false;
    const s = state();
    let tx = s.rpgSpiritualAttack;
    if (!tx && (!effect() || strike.disabled)) return false;
    running = true;
    draw();
    try {
      if (!tx) {
        const active = effect();
        const net = RPGConnect.getStatus();
        if (net.controlled && !net.target) {
          RPGConnect.openTargetPicker();
          ribbon('Sélectionne une cible Encounter');
          return false;
        }
        const turn = s.turn;
        const used = usage() || {turn};
        const a = await makeAttackRoll(8, 'Arme spirituelle');
        if (!a || s.turn !== turn || !effect() || (s.eco.b && !usage())) return false;
        const before = used.before || JSON.parse(JSON.stringify(s));
        const actionId = used.actionId || crypto.randomUUID();
        window.RPGResources?.begin(actionId, before);
        commitAttack(a);
        s.eco.b = true;
        s.spiritualBonus = {turn, initial: !!used.initial, moved: !!used.moved, struck: true};
        tx = {
          before, actionId, attackId: crypto.randomUUID(),
          combatId: net.controlled ? RPGHealth.getContext().combatId : null,
          targetId: net.controlled ? net.target.id : null,
          level: active.level, roll: a, phase: 'hit'
        };
        s.rpgSpiritualAttack = tx;
        bridge.healthRefresh();
      }
      if (tx.phase === 'hit') {
        const hit = await askHit('Arme spirituelle', {...tx.roll, kind: 'spell', transaction: tx});
        if (s.rpgSpiritualAttack !== tx) return false;
        tx.phase = hit ? 'damage' : 'miss';
        bridge.healthRefresh();
      }
      if (tx.phase === 'damage') {
        const critical = tx.roll.nat === 20;
        const dice = roll(diceCount(tx.level) * (critical ? 2 : 1), 8);
        const amount = dice.sum + 4;
        window.RPGUndo?.reserve(tx.actionId, tx.before);
        tx.damage = {
          undoCapture: window.RPGUndo?.describe(tx.actionId) || [],
          attackId: tx.attackId, actionId: tx.actionId, combatId: tx.combatId,
          targetId: tx.targetId, actor: 'zephyr', attackKind: 'spell',
          source: 'Arme spirituelle', amount, components: [{amount, type: 'force'}],
          spiritualWeapon: {level: tx.level, dice: dice.a, natural: tx.roll.nat},
          undoCertified: true
        };
        tx.phase = 'sent';
        s.dmg += amount;
        bridge.healthRefresh();
        if (tx.combatId && RPGConnect.getStatus().controlled) ZephyrCombat.submit(tx.damage);
        card.dataset.fx = 'strike';
        setTimeout(() => delete card.dataset.fx, 500);
        addLog('Arme spirituelle', dice.a.join(' + ') + ' + 4 = ' + amount + ' force' +
          (critical ? ' · CRITIQUE' : ''), 'attack');
      }
      if (tx.phase === 'miss') addLog('Arme spirituelle', 'RATÉ · action bonus utilisée', 'attack');
      s.rpgSpiritualAttack = null;
      bridge.healthRefresh();
      return true;
    } finally {
      running = false;
      draw();
    }
  }

  strike.onclick = attack;
  move.onclick = moveWeapon;
  dismiss.onclick = dismissWeapon;
  window.SpiritualWeapon = {effect, attack, activate, draw};
  CompanionAPI.subscribe(event => {
    if (['state:changed', 'effect:feedback'].includes(event.type)) draw();
  });
  for (const event of ['rpg-table:context', 'rpg-table:mode', 'rpg-resolution:change']) {
    window.addEventListener(event, draw);
  }
  RPGResolution.register('spiritual-weapon', {
    detach: () => {
      const old = state().rpgSpiritualAttack;
      // A local roll can resume after reload even when Table Libre is already active.
      if (!old?.combatId) return null;
      state().rpgSpiritualAttack = null;
      return old;
    }
  });
  draw();
  if (state().rpgSpiritualAttack) setTimeout(attack, 0);
})();
