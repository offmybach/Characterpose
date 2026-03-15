const modal = document.getElementById('magazineModal');
const openBtn = document.getElementById('openMagazine');
const closeBtn = document.getElementById('closeMagazineBtn');
const closeOverlay = document.getElementById('closeMagazine');
const magazine = document.getElementById('magazineBook');
const slotTemplate = document.getElementById('couponSlotTemplate');
const stageTilt = document.querySelector('.stage-tilt');
const nextHotspot = document.getElementById('turnNext');
const prevHotspot = document.getElementById('turnPrev');

const frontCoverInput = document.getElementById('frontCoverInput');
const backCoverInput = document.getElementById('backCoverInput');
const frontCoverSlot = document.getElementById('frontCoverSlot');
const backCoverSlot = document.getElementById('backCoverSlot');
const frontCoverPreview = document.getElementById('frontCoverPreview');
const backCoverPreview = document.getElementById('backCoverPreview');
const clarenceImageInput = document.getElementById('clarenceImageInput');
const clarenceImageSlot = document.getElementById('clarenceImageSlot');
const clarenceImageMain = document.getElementById('clarenceImageMain');
const clarenceEcho1 = document.getElementById('clarenceEcho1');
const clarenceEcho2 = document.getElementById('clarenceEcho2');
const uploadStatus = document.getElementById('uploadStatus');

const sheetCount = 3;
let current = 0;

const memoryStore = new Map();

function setUploadStatus(message, tone = 'ok') {
  if (!uploadStatus) return;
  uploadStatus.textContent = message;
  uploadStatus.dataset.tone = tone;
}

function hasMagazineMarkup() {
  return Boolean(modal && openBtn && closeBtn && closeOverlay && magazine && slotTemplate && stageTilt);
}

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
    // Keep in memory when local storage is unavailable
  }
}

function isImageFile(file) {
  if (!file) return false;
  return (file.type && file.type.startsWith('image/')) || /\.(png|jpe?g|gif|webp|svg|bmp|avif|heic|heif)$/i.test(file.name || '');
}

function setCoverImage(dataUrl, targetImg) {
  if (!targetImg) return;
  const placeholderText = targetImg.parentElement?.querySelector('.cover-placeholder__text');
  if (dataUrl) {
    targetImg.src = dataUrl;
    targetImg.hidden = false;
    if (placeholderText) placeholderText.hidden = true;
  } else {
    targetImg.hidden = true;
    if (placeholderText) placeholderText.hidden = false;
  }
}

function applyFrontCover(dataUrl) {
  setCoverImage(dataUrl, frontCoverPreview);
}

function applyBackCover(dataUrl) {
  setCoverImage(dataUrl, backCoverPreview);
}

function applyClarenceImage(dataUrl) {
  [clarenceImageMain, clarenceEcho1, clarenceEcho2].forEach((img) => {
    if (!img) return;
    img.src = dataUrl;
    img.hidden = !dataUrl;
    const fallback = img.parentElement?.querySelector('span');
    if (fallback) fallback.hidden = Boolean(dataUrl);
  });
}

function readFileToDataUrl(file, done) {
  if (!isImageFile(file)) {
    setUploadStatus('Please choose an image file (PNG, JPG, WEBP, etc).', 'error');
    return;
  }
  const reader = new FileReader();
  reader.onload = () => {
    done(String(reader.result || ''));
    setUploadStatus(`Uploaded: ${file.name}`, 'ok');
  };
  reader.onerror = () => setUploadStatus('Could not read that image file. Please try another one.', 'error');
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

function beep() {
  const ctx = new (window.AudioContext || window.webkitAudioContext)();
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  osc.type = 'triangle';
  osc.frequency.value = 500;
  gain.gain.setValueAtTime(0.08, ctx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.13);
  osc.connect(gain);
  gain.connect(ctx.destination);
  osc.start();
  osc.stop(ctx.currentTime + 0.13);
}

function createCouponBlock(text = 'Editable coupon text goes here') {
  const block = document.createElement('article');
  block.className = 'coupon-slot';
  block.contentEditable = 'true';

  const copy = document.createElement('p');
  copy.textContent = text;
  block.appendChild(copy);

  const cut = document.createElement('div');
  cut.className = 'coupon-slot__cutline';
  cut.contentEditable = 'true';
  cut.textContent = 'Editable dotted cut-line text';
  block.appendChild(cut);

  return block;
}

function createPageHeader() {
  const header = document.createElement('div');
  header.className = 'coupon-page__header';

  const mast = document.createElement('div');
  mast.className = 'coupon-page__masthead';
  mast.contentEditable = 'true';
  mast.setAttribute('aria-label', 'Store title');
  mast.textContent = '';

  const sub = document.createElement('div');
  sub.className = 'coupon-page__sub';
  sub.contentEditable = 'true';
  sub.textContent = 'Extra Savings';

  const title = document.createElement('div');
  title.className = 'coupon-page__hero-title';
  title.contentEditable = 'true';
  title.textContent = 'COUPONS';

  header.append(mast, sub, title);
  return header;
}

function makeCouponPage(pageNumber) {
  const page = document.createElement('section');
  page.className = 'page-face coupon-page';

  const header = createPageHeader();
  const grid = document.createElement('div');
  grid.className = 'coupon-grid';

  const starter = [
    'TAKE AN EXTRA 10% OFF ALL CLEARANCE TOYS!',
    '$5.00 OFF ALL SMART ROBOTS',
    'BUY ONE GAME, GET ONE HALF PRICE!'
  ];

  starter.forEach((line) => grid.appendChild(createCouponBlock(line)));

  const num = document.createElement('span');
  num.className = 'coupon-page__number';
  num.textContent = String(pageNumber);

  page.append(header, grid, num);
  return page;
}

function makeOpenNotePage(pageNumber) {
  const page = document.createElement('section');
  page.className = 'page-face coupon-page coupon-page--open';
  const header = createPageHeader();
  const note = document.createElement('div');
  note.className = 'coupon-page__open-note';
  note.contentEditable = 'true';
  note.textContent = 'Open page space for upcoming content.';
  const num = document.createElement('span');
  num.className = 'coupon-page__number';
  num.textContent = String(pageNumber);
  page.append(header, note, num);
  return page;
}

function buildMagazine() {
  if (!magazine) return;
  magazine.innerHTML = '';
  for (let i = 0; i < sheetCount; i += 1) {
    const sheet = document.createElement('article');
    sheet.className = 'sheet';
    sheet.style.zIndex = String(sheetCount - i);

    const leftPageNo = i * 2 + 1;
    const rightPageNo = leftPageNo + 1;

    const front = leftPageNo <= 4 ? makeCouponPage(leftPageNo) : makeOpenNotePage(leftPageNo);
    const back = rightPageNo <= 4 ? makeCouponPage(rightPageNo) : makeOpenNotePage(rightPageNo);

    front.classList.add('page-front');
    back.classList.add('page-back');
    sheet.append(front, back);
    magazine.appendChild(sheet);
  }
}

function updateFlips() {
  if (!magazine) return;
  magazine.classList.toggle('magazine--closed', current === 0);
  [...magazine.children].forEach((sheet, idx) => {
    sheet.classList.toggle('flipped', idx < current);
    sheet.style.zIndex = idx < current ? String(idx + 1) : String(sheetCount - idx);
  });
}

function goForward(playSound = true) {
  if (current < sheetCount) {
    current += 1;
    updateFlips();
    if (playSound) beep();
  }
}

function goBack(playSound = true) {
  if (current > 0) {
    current -= 1;
    updateFlips();
    if (playSound) beep();
  }
}

function openMagazine() {
  if (!hasMagazineMarkup()) return;
  const dockRect = openBtn.getBoundingClientRect();
  const centerX = window.innerWidth / 2;
  const centerY = window.innerHeight / 2;
  const dockX = dockRect.left + dockRect.width / 2;
  const dockY = dockRect.top + dockRect.height / 2;
  stageTilt.style.setProperty('--launch-x', `${Math.round(dockX - centerX)}px`);
  stageTilt.style.setProperty('--launch-y', `${Math.round(dockY - centerY)}px`);

  modal.classList.add('open');
  modal.setAttribute('aria-hidden', 'false');

  if (current === 0) {
    window.setTimeout(() => goForward(false), 230);
  }
}

function closeMagazineModal() {
  if (!modal) return;
  modal.classList.remove('open');
  modal.setAttribute('aria-hidden', 'true');
}

window.addEventListener('dragover', (event) => event.preventDefault());
window.addEventListener('drop', (event) => event.preventDefault());

applyFrontCover(getSavedValue('clarence-front-cover'));
applyBackCover(getSavedValue('clarence-back-cover'));
wireImageInput(frontCoverInput, 'clarence-front-cover', applyFrontCover);
wireImageInput(backCoverInput, 'clarence-back-cover', applyBackCover);
wireDropAndClick(frontCoverSlot, frontCoverInput, 'clarence-front-cover', applyFrontCover);
wireDropAndClick(backCoverSlot, backCoverInput, 'clarence-back-cover', applyBackCover);

applyClarenceImage(getSavedValue('clarence-character-image'));
wireImageInput(clarenceImageInput, 'clarence-character-image', applyClarenceImage);
wireDropAndClick(clarenceImageSlot, clarenceImageInput, 'clarence-character-image', applyClarenceImage);

setUploadStatus('Tip: cover slots use a 3:2 shape. Drop or click to upload.', 'ok');

if (magazine) {
  magazine.addEventListener('click', (event) => {
    const bounds = magazine.getBoundingClientRect();
    const x = event.clientX - bounds.left;
    const y = event.clientY - bounds.top;
    if (y <= bounds.height * 0.58) return;
    if (x > bounds.width * 0.72) goForward();
    if (x < bounds.width * 0.28) goBack();
  });
}

openBtn?.addEventListener('click', openMagazine);
openBtn?.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault();
    openMagazine();
  }
});
closeBtn?.addEventListener('click', closeMagazineModal);
closeOverlay?.addEventListener('click', closeMagazineModal);
nextHotspot?.addEventListener('click', goForward);
prevHotspot?.addEventListener('click', goBack);

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') closeMagazineModal();
  if (event.key === 'ArrowRight') goForward();
  if (event.key === 'ArrowLeft') goBack();
});

if (hasMagazineMarkup()) {
  buildMagazine();
  updateFlips();
} else {
  setUploadStatus('Files are out of sync. Please copy newest index.html, style.css, and script.js together.', 'error');
}
