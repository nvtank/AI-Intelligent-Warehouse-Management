import { renderToStaticMarkup } from "react-dom/server";
import { expect, it } from "vitest";
import { FoundationContent } from "./App";

it("labels the simulation and leaves future features unavailable", () => {
  const html = renderToStaticMarkup(<FoundationContent />);
  expect(html).toContain("Môi trường mô phỏng");
  expect(html).toContain("Không sử dụng dữ liệu kho thật");
  expect(html).toContain("Chưa có dữ liệu kho");
  expect(html.match(/Chưa triển khai/g)).toHaveLength(5);
  expect(html).not.toContain("<form");
});
