import { Logger as LoggerInterface } from "@/data-access/interfaces";
import logger from "@/lib/logger";
import { Logger as WinstonLogger } from "winston";

export class Logger implements LoggerInterface {
  private logger: WinstonLogger;

  constructor() {
    this.logger = logger;
  }

  error(...message: any[]): void {
    this.logger.error(message);
  }

  info(...message: any[]): void {
    this.logger.info(message);
  }

  warn(...message: any[]): void {
    this.logger.warn(message);
  }
}
