import { screen } from "./research.mjs";
self.onmessage = ({ data }) => {
  try {
    self.postMessage({ result: screen(data.parameters, data.options) });
  } catch (e) {
    self.postMessage({ error: e.message });
  }
};
