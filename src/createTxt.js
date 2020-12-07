import { saveAs } from 'file-saver';

const createTxt = (words) => {
  const blob = new Blob([words], { type: 'text/plain;charset=utf-8' });
  const filename = Math.floor(Date.now() / 1000);
  return saveAs(blob, `${filename}.txt`);
};

export default createTxt;
