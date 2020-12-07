import $ from 'jquery';
import 'bootstrap';
import createTxt from './createTxt';
// import createPdf from './createPdf';

const save = (id) => {
  const words = $(id).val();
  if (words.length > 0) {
    createTxt(words);
  }
};

$('document').ready(() => {
  // eslint-disable-next-line func-names
  $('#tabText a').on('click', function (e) {
    e.preventDefault();
    $(this).tab('show');
  });
  // eslint-disable-next-line func-names
  $('#tabResult a').on('click', function (e) {
    e.preventDefault();
    $(this).tab('show');
  });
  $('#send').click(() => {
    const text1 = $('#text1').val();
    const text2 = $('#text2').val();
    const option = $('input[name="options"]:checked').val();
    // 1 - regular; 2 - frequency; 3 - lexical minimums; 4 - dictionary
    if (option === '1') {
      $.ajax({
        url: 'http://localhost:5000/api/',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
          text1, text2,
        }),
      }).done((data) => {
        const result1 = JSON.stringify(data.text1).replace(/["[\]{}]*/g, '');
        const result2 = JSON.stringify(data.text2).replace(/["[\]{}]*/g, '');
        $('#result1').empty();
        $('#result2').empty();
        $('#intersection').empty();
        $('#result1').append(result1.replace(/,/g, '\r\n'));
        $('#result2').append(result2.replace(/,/g, '\r\n'));
        $('#intersection').append(data.intersection.join('\r\n'));
      });
    }
    if (option === '2') {
      $.ajax({
        url: 'http://localhost:5000/api/freq/',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
          text1, text2,
        }),
      }).done((data) => {
        const result1 = JSON.stringify(data.text1).replace(/["[\]{}]*/g, '');
        const result2 = JSON.stringify(data.text2).replace(/["[\]{}]*/g, '');
        $('#result1').empty();
        $('#result2').empty();
        $('#intersection').empty();
        $('#result1').append(result1.replace(/,/g, '\r\n'));
        $('#result2').append(result2.replace(/,/g, '\r\n'));
        $('#intersection').append(data.intersection.join('\r\n'));
      });
    }
    if (option === '3') {
      $.ajax({
        url: 'http://localhost:5000/api/lex/',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
          text1, text2,
        }),
      }).done((data) => {
        const result1 = JSON.stringify(data.text1).replace(/["[\]{}]*/g, '');
        const result2 = JSON.stringify(data.text2).replace(/["[\]{}]*/g, '');
        $('#result1').empty();
        $('#result2').empty();
        $('#intersection').empty();
        if (data.text1_a1 && data.text1_a2) {
          $('#result1').append(`A1: ${Math.trunc(data.text1_a1 * 100)}%; A2: ${Math.trunc(data.text1_a2 * 100)}%\r\n\r\n`);
        }
        if (data.text2_a1 && data.text2_a2) {
          $('#result2').append(`A1: ${Math.trunc(data.text2_a1 * 100)}%; A2: ${Math.trunc(data.text2_a2 * 100)}%\r\n\r\n`);
        }
        $('#result1').append(result1.replace(/,/g, '\r\n'));
        $('#result2').append(result2.replace(/,/g, '\r\n'));
        $('#intersection').append(data.intersection.join('\r\n'));
      });
    }
    if (option === '4') {
      let targetLanguageCode = '';
      targetLanguageCode = $('#targetLanguageCode').val();
      if (targetLanguageCode.length === 0) { targetLanguageCode = 'en'; }
      $.ajax({
        url: 'http://localhost:5000/api/dict/',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
          text1, text2, targetLanguageCode,
        }),
      }).done((data) => {
        const result1 = JSON.stringify(data.text1).replace(/["[\]{}]*/g, '');
        const result2 = JSON.stringify(data.text2).replace(/["[\]{}]*/g, '');
        $('#result1').empty();
        $('#result2').empty();
        $('#intersection').empty();
        $('#result1').append(result1.replace(/,/g, '\r\n'));
        $('#result2').append(result2.replace(/,/g, '\r\n'));
        $('#intersection').append(data.intersection.join('\r\n'));
      });
    }
  });
  $('#saveResult').click(() => {
    if ($('#nav-result1').hasClass('active')) {
      save('#result1');
      return;
    }
    if ($('#nav-result2').hasClass('active')) {
      save('#result2');
      return;
    }
    if ($('#nav-intersection').hasClass('active')) {
      save('#intersection');
    }
  });
});
