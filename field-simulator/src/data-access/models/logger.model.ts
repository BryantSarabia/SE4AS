import { Logger as WinstonLogger } from "winston";
import { Logger as LoggerInterface } from "../../data-access/interfaces";
import logger from "../../lib/logger";

export class Logger implements LoggerInterface {
  private logger: WinstonLogger;

  constructor() {
    this.logger = logger;
  }

  error(...message: unknown[]): void {
    this.logger.error(message);
  }

  info(...message: unknown[]): void {
    this.logger.info(message);
  }

  warn(...message: unknown[]): void {
    this.logger.warn(message);
  }
}
