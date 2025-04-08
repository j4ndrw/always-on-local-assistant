/* eslint-disable @typescript-eslint/no-explicit-any */
export const sleep = (ms: number) => new Promise((res) => setTimeout(res, ms));

export const debounce = <T extends (...args: any[]) => any>(
  cb: T,
  waitMs: number,
) => {
  let timeout: NodeJS.Timeout | undefined;
  const callable = (...args: any) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => cb(...args), waitMs);
  };
  return callable as T;
};

export const throttle = <T extends (...args: any[]) => any>(
  cb: T,
  waitMs: number,
) => {
  let wait = false;
  return ((...args: any[]) => {
    if (wait) return;

    cb(...args);

    wait = true;
    setTimeout(() => (wait = false), waitMs);
  }) as T;
};
