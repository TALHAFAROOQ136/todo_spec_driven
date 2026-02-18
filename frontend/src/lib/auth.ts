import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";
import { Pool } from "pg";

const trustedOrigins = [
  process.env.BETTER_AUTH_URL,
  process.env.BETTER_AUTH_TRUSTED_ORIGINS,
].filter(Boolean) as string[];

export const auth = betterAuth({
  database: new Pool({
    connectionString: process.env.DATABASE_URL!,
  }),
  emailAndPassword: {
    enabled: true,
  },
  plugins: [
    jwt(),
  ],
  secret: process.env.BETTER_AUTH_SECRET,
  trustedOrigins,
});
