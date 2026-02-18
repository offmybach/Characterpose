const modal = document.getElementById('magazineModal');
const openBtn = document.getElementById('openMagazine');
const closeBtn = document.getElementById('closeMagazineBtn');
const closeOverlay = document.getElementById('closeMagazine');
const magazine = document.getElementById('magazineBook');
const slotTemplate = document.getElementById('couponSlotTemplate');

const frontCoverInput = document.getElementById('frontCoverInput');
const backCoverInput = document.getElementById('backCoverInput');
const frontCoverSlot = document.getElementById('frontCoverSlot');
const backCoverSlot = document.getElementById('backCoverSlot');
const frontCoverPreview = document.getElementById('frontCoverPreview');
const backCoverPreview = document.getElementById('backCoverPreview');
const magazineFrontPreview = document.getElementById('magazineFrontPreview');

const pageData = [
  { title: 'Front Cover Coupon Spread', theme: 'Welcome and Starter Offers' },
  { title: 'Coupon Page 2', theme: 'Smart Saver Challenges' },
  { title: 'Coupon Page 3', theme: 'Reading Night Rewards' },
  { title: 'Coupon Page 4', theme: 'Classroom Value Deals' },
  { title: 'Coupon Page 5', theme: 'Family Bundle Savings' },
  { title: 'Back Cover Coupons', theme: 'Final Bonus & Thank You' }
];

const sheetCount = 3;
let current = 0;

const memoryStore = new Map();
function getSavedValue(key) {
  try {
    return localStorage.getItem(key) || memoryStore.get(key) || '';
  } catch {
    return memoryStore.get(key) || '';
  }
}

function saveValue(key, value) {
  memoryStore.set(key, value);
  try {
    localStorage.setItem(key, value);
  } catch {
    // Continue with in-memory storage when localStorage is unavailable
  }
}

function setCoverImage(dataUrl, targetImg) {
  if (!targetImg) return;
  if (dataUrl) {
    targetImg.src = dataUrl;
    targetImg.hidden = false;
    const txt = targetImg.parentElement?.querySelector('.cover-placeholder__text, .magazine-preview__tag');
    if (txt) txt.hidden = true;
  } else {
    targetImg.hidden = true;
    const txt = targetImg.parentElement?.querySelector('.cover-placeholder__text, .magazine-preview__tag');
    if (txt) txt.hidden = false;
  }
}

function applyFrontCover(dataUrl) {
  setCoverImage(dataUrl, frontCoverPreview);
  setCoverImage(dataUrl, magazineFrontPreview);
}

function applyBackCover(dataUrl) {
  setCoverImage(dataUrl, backCoverPreview);
}

function readFileToDataUrl(file, done) {
  if (!file || !file.type.startsWith('image/')) return;
  const reader = new FileReader();
  reader.onload = () => done(String(reader.result || ''));
  reader.readAsDataURL(file);
}

function wireImageInput(input, storageKey, applyFn) {
  if (!input) return;
  input.addEventListener('change', () => {
    const file = input.files?.[0];
    readFileToDataUrl(file, (dataUrl) => {
      saveValue(storageKey, dataUrl);
      applyFn(dataUrl);
    });
  });
}

function wireDropAndClick(slot, input, storageKey, applyFn) {
  if (!slot || !input) return;

  slot.addEventListener('click', () => input.click());
  slot.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      input.click();
    }
  });

  ['dragenter', 'dragover'].forEach((evtName) => {
    slot.addEventListener(evtName, (event) => {
      event.preventDefault();
      slot.classList.add('is-dragover');
    });
  });

  ['dragleave', 'dragend', 'drop'].forEach((evtName) => {
    slot.addEventListener(evtName, () => slot.classList.remove('is-dragover'));
  });

  slot.addEventListener('drop', (event) => {
    event.preventDefault();
    const file = event.dataTransfer?.files?.[0];
    readFileToDataUrl(file, (dataUrl) => {
      saveValue(storageKey, dataUrl);
      applyFn(dataUrl);
    });
  });
}

window.addEventListener('dragover', (event) => event.preventDefault());
window.addEventListener('drop', (event) => event.preventDefault());

applyFrontCover(getSavedValue('clarence-front-cover'));
applyBackCover(getSavedValue('clarence-back-cover'));
wireImageInput(frontCoverInput, 'clarence-front-cover', applyFrontCover);
wireImageInput(backCoverInput, 'clarence-back-cover', applyBackCover);
wireDropAndClick(frontCoverSlot, frontCoverInput, 'clarence-front-cover', applyFrontCover);
wireDropAndClick(backCoverSlot, backCoverInput, 'clarence-back-cover', applyBackCover);

function beep() {
  const ctx = new (window.AudioContext || window.webkitAudioContext)();
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  osc.type = 'triangle';
  osc.frequency.value = 510;
  gain.gain.setValueAtTime(0.08, ctx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.12);
  osc.connect(gain);
  gain.connect(ctx.destination);
  osc.start();
  osc.stop(ctx.currentTime + 0.12);
}

function makeCouponSlot(index) {
  const slot = slotTemplate.content.firstElementChild.cloneNode(true);
  slot.querySelector('h4').textContent = `Coupon ${index}`;
  slot.querySelector('p').textContent = 'Editable details and instructions. Resize this coupon box if you need more room.';
  slot.querySelector('.coupon-slot__offer').textContent = `$${index} OFF`;
  return slot;
}

function makeCouponPage(data) {
  const page = document.createElement('section');
  page.className = 'page-face coupon-page';

  const heading = document.createElement('h3');
  heading.className = 'coupon-page__title';
  heading.textContent = `${data.title} • ${data.theme}`;
  heading.contentEditable = 'true';

  const grid = document.createElement('div');
  grid.className = 'coupon-grid';
  for (let i = 1; i <= 4; i++) {
    grid.appendChild(makeCouponSlot(i));
  }

  page.append(heading, grid);
  return page;
}

function buildMagazine() {
  magazine.innerHTML = '';
  for (let i = 0; i < sheetCount; i++) {
    const sheet = document.createElement('article');
    sheet.className = 'sheet';
    sheet.style.zIndex = String(sheetCount - i);

    const front = makeCouponPage(pageData[i * 2]);
    const back = makeCouponPage(pageData[i * 2 + 1]);

    front.classList.add('page-front');
    back.classList.add('page-back');

    sheet.append(front, back);
    magazine.appendChild(sheet);
  }
}

function updateFlips() {
  [...magazine.children].forEach((sheet, idx) => {
    sheet.classList.toggle('flipped', idx < current);
    sheet.style.zIndex = idx < current ? String(idx + 1) : String(sheetCount - idx);
  });
}

magazine.addEventListener('click', (event) => {
  const bounds = magazine.getBoundingClientRect();
  const x = event.clientX - bounds.left;
  const y = event.clientY - bounds.top;

  if (y <= bounds.height * 0.64) return;

  if (x > bounds.width * 0.7 && current < sheetCount) {
    current += 1;
    updateFlips();
    beep();
  } else if (x < bounds.width * 0.3 && current > 0) {
    current -= 1;
    updateFlips();
    beep();
  }
});

function openMagazine() {
  modal.classList.add('open');
  modal.setAttribute('aria-hidden', 'false');
}

function closeMagazineModal() {
  modal.classList.remove('open');
  modal.setAttribute('aria-hidden', 'true');
}

openBtn.addEventListener('click', openMagazine);
openBtn.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault();
    openMagazine();
  }
});

closeBtn.addEventListener('click', closeMagazineModal);
closeOverlay.addEventListener('click', closeMagazineModal);
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') closeMagazineModal();
});

buildMagazine();
updateFlips();
