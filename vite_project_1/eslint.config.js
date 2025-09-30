// eslint.config.js
import js from '@eslint/js'
import tseslint from 'typescript-eslint'
import svelte from 'eslint-plugin-svelte'
import svelteParser from 'svelte-eslint-parser'

export default [
  // Ignore build artifacts & deps
  { ignores: ['dist', 'build', 'node_modules'] },

  // Base JS rules
  js.configs.recommended,

  // TypeScript rules (covers *.ts by default)
  ...tseslint.configs.recommended,

  // Svelte rules (flat config)
  ...svelte.configs['flat/recommended'],

  // Make Svelte <script> blocks use the TS parser
  {
    files: ['**/*.svelte'],
    languageOptions: {
      parser: svelteParser,
      parserOptions: {
        // Use TypeScript parser inside <script> blocks
        parser: tseslint.parser
      }
    }
  }
]
