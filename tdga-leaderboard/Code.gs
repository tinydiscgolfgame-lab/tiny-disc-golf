/**
 * Tiny Disc Golf — TDGA Global Leaderboard backend
 *
 * Use this as a script bound to your own Google Sheet:
 * 1. Create a blank Google Sheet.
 * 2. Open Extensions > Apps Script.
 * 3. Replace the editor contents with this file and save.
 * 4. Run setupLeaderboard once and authorize it.
 * 5. Deploy > New deployment > Web app.
 *    Execute as: Me
 *    Who has access: Anyone
 * 6. Send the deployed URL ending in /exec to the app maintainer.
 *
 * Players submit to the Submissions sheet. Nothing appears publicly until
 * you change its Status from PENDING to APPROVED. The public endpoint only
 * returns approved rows.
 */

const SUBMISSIONS_SHEET = 'Submissions';
const HEADERS = ['Submitted At', 'Player Name', 'Ranking', 'Status'];

function setupLeaderboard() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(SUBMISSIONS_SHEET);
  if (!sheet) sheet = ss.insertSheet(SUBMISSIONS_SHEET);
  if (sheet.getLastRow() === 0) {
    sheet.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS]);
    sheet.setFrozenRows(1);
    sheet.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold');
    sheet.setColumnWidth(1, 175);
    sheet.setColumnWidth(2, 220);
    sheet.setColumnWidth(3, 100);
    sheet.setColumnWidth(4, 130);
  }
  const statusRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(['PENDING', 'APPROVED', 'REJECTED'], true)
    .setAllowInvalid(false)
    .build();
  if (sheet.getMaxRows() > 1) {
    sheet.getRange(2, 4, sheet.getMaxRows() - 1, 1).setDataValidation(statusRule);
  }
  return 'Ready. Review submissions in the Submissions sheet.';
}

function doGet(e) {
  const action = String((e && e.parameter && e.parameter.action) || 'leaderboard');
  if (action !== 'leaderboard') {
    return output_({ ok: false, error: 'Unknown action' }, e);
  }
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(SUBMISSIONS_SHEET);
  if (!sheet || sheet.getLastRow() < 2) return output_({ ok: true, players: [] }, e);

  const rows = sheet.getRange(2, 1, sheet.getLastRow() - 1, HEADERS.length).getValues();
  const players = rows
    .filter(row => String(row[3]).trim().toUpperCase() === 'APPROVED')
    .map(row => ({
      name: String(row[1] || '').trim(),
      ranking: Number(row[2]),
      approvedAt: row[0] instanceof Date ? row[0].toISOString() : String(row[0] || '')
    }))
    .filter(p => p.name && Number.isFinite(p.ranking))
    .sort((a, b) => b.ranking - a.ranking || a.name.localeCompare(b.name))
    .map((p, i) => ({ rank: i + 1, ...p }));

  return output_({ ok: true, players: players }, e);
}

function doPost(e) {
  try {
    const params = (e && e.parameter) || {};
    const name = String(params.playerName || '').trim().replace(/\s+/g, ' ');
    const rankingRaw = String(params.ranking || '').trim();
    const ranking = Number(rankingRaw);

    if (!name || name.length > 50) {
      return output_({ ok: false, error: 'Enter a player name up to 50 characters.' }, e);
    }
    if (!rankingRaw || !Number.isFinite(ranking) || ranking < 0 || ranking > 1000) {
      return output_({ ok: false, error: 'Enter a numeric ranking between 0 and 1000.' }, e);
    }

    const lock = LockService.getScriptLock();
    lock.waitLock(10000);
    try {
      const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SUBMISSIONS_SHEET);
      if (!sheet) throw new Error('Run setupLeaderboard first.');
      sheet.appendRow([new Date(), name, ranking, 'PENDING']);
    } finally {
      lock.releaseLock();
    }
    return output_({ ok: true, message: 'Submitted for approval.' }, e);
  } catch (err) {
    return output_({ ok: false, error: String(err && err.message || err) }, e);
  }
}

function output_(data, e) {
  const json = JSON.stringify(data);
  const callback = String((e && e.parameter && e.parameter.callback) || '');
  if (callback) {
    if (!/^[A-Za-z_$][0-9A-Za-z_$\.]*$/.test(callback)) {
      return ContentService.createTextOutput('/* invalid callback */')
        .setMimeType(ContentService.MimeType.JAVASCRIPT);
    }
    return ContentService.createTextOutput(callback + '(' + json + ');')
      .setMimeType(ContentService.MimeType.JAVASCRIPT);
  }
  return ContentService.createTextOutput(json)
    .setMimeType(ContentService.MimeType.JSON);
}
