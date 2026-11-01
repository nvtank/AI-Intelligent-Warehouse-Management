import { Link, Route, Routes } from "react-router";
import { HealthStatus } from "./HealthStatus";

const milestones = [
  { code: "M1", title: "Nền tảng hệ thống", detail: "Ứng dụng web, API, PostgreSQL và kiểm tra tự động.", current: true },
  { code: "M2", title: "Cấu trúc & dữ liệu mô phỏng", detail: "Schema, migration và dữ liệu kho mẫu.", current: false },
  { code: "M3", title: "Đăng nhập & phân quyền", detail: "Admin, Quản lý kho và Nhân viên kho.", current: false },
  { code: "M4", title: "Danh mục vật liệu", detail: "SKU, hình ảnh, quy cách và tìm kiếm tiếng Việt.", current: false },
  { code: "M5", title: "Bản đồ kho 2D", detail: "Zone, lối đi, kệ, bin và tầng kệ.", current: false },
  { code: "M6", title: "Quản lý đơn hàng", detail: "Đơn nhập/xuất, dòng hàng và trạng thái.", current: false },
];

export function FoundationContent() {
  return (
    <>
      <div className="eyebrow">PHASE A / FOUNDATION</div>
      <h1>Nền tảng cho một<br />kho hàng rõ ràng hơn.</h1>
      <p className="intro">MapFlow AI đang được xây dựng từng mốc. Bắt đầu từ nền tảng để quản lý vật liệu, không gian kho và đơn hàng.</p>
      <div className="simulation-note"><span aria-hidden="true">◎</span> Môi trường mô phỏng · Không sử dụng dữ liệu kho thật</div>
      <section className="roadmap" aria-labelledby="roadmap-heading">
        <div className="section-heading">
          <h2 id="roadmap-heading">Lộ trình triển khai</h2>
          <span>6 mốc chức năng · M7 kiểm tra hoàn thiện</span>
        </div>
        <div className="milestone-grid">
          {milestones.map((milestone) => (
            <article key={milestone.code} className={`milestone ${milestone.current ? "milestone-current" : ""}`}>
              <div className="milestone-top">
                <span className="milestone-code">{milestone.code}</span>
                <span className="milestone-state">{milestone.current ? "Mốc hiện tại" : "Chưa triển khai"}</span>
              </div>
              <h3>{milestone.title}</h3>
              <p>{milestone.detail}</p>
            </article>
          ))}
        </div>
      </section>
      <p className="empty-note">Chưa có dữ liệu kho ở mốc này. Dữ liệu mẫu được bổ sung tại M2 sau khi xác nhận.</p>
    </>
  );
}

function Home() {
  return <><FoundationContent /><HealthStatus /></>;
}

export function App() {
  return (
    <div className="app-shell">
      <a href="#main" className="skip-link">Đến nội dung chính</a>
      <header className="app-header">
        <Link to="/" className="brand" aria-label="MapFlow AI — Trang chủ">
          <span className="brand-mark" aria-hidden="true">M<span>↗</span></span>
          <span>MapFlow <span className="brand-ai">AI</span></span>
        </Link>
        <span className="environment-badge">KHO MÔ PHỎNG</span>
      </header>
      <main id="main">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="*" element={<div className="not-found"><h1>Không tìm thấy trang</h1><Link to="/">Về trang chủ</Link></div>} />
        </Routes>
      </main>
      <footer>MapFlow AI <span>Phase A · M1 Foundation</span></footer>
    </div>
  );
}
