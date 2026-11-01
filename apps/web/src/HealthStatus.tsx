import { useQuery } from "@tanstack/react-query";
import { getHealth } from "./api/client";

export function HealthStatus() {
  const health = useQuery({
    queryKey: ["health"],
    queryFn: ({ signal }) => getHealth(signal),
    staleTime: 30_000,
  });

  if (health.isPending) {
    return <p role="status" className="connection">Đang kiểm tra kết nối API…</p>;
  }
  if (health.isError) {
    return (
      <div role="alert" className="connection connection-error">
        <p>Chưa kết nối được API. Kiểm tra dịch vụ và cấu hình URL.</p>
        <button type="button" onClick={() => void health.refetch()}>Thử lại</button>
      </div>
    );
  }
  return (
    <p role="status" className="connection">
      <span className="status-dot" aria-hidden="true" />
      API đang hoạt động <span className="api-version">v{health.data.version}</span>
    </p>
  );
}
