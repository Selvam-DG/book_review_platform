export function timeAgo(dateString?: string): string {
  if (!dateString) return "";
  const diff = Date.now() - new Date(dateString).getTime();
  const seconds = diff / 1000;

  if (seconds < 60) return `${Math.floor(seconds)}s ago`;
  const minutes = seconds / 60;
  if (minutes < 60) return `${Math.floor(minutes)}m ago`;
  const hours = minutes / 60;
  if (hours < 24) return `${Math.floor(hours)}h ago`;
  const days = hours / 24;
  if (days < 7) return `${Math.floor(days)} days ago`;
  const weeks = days / 7;
  if (weeks < 4) return `${Math.floor(weeks)} weeks ago`;
  const months = days / 30;
  if (months < 12) return `${Math.floor(months)} months ago`;
  const years = days / 365;
  return `${Math.floor(years)} years ago`;
}