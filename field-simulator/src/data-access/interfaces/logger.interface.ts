export interface Logger {
  error: (...message: any[]) => void;
  info: (...message: any[]) => void;
  warn: (...message: any[]) => void;
}
