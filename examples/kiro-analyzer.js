#!/usr/bin/env node

/**
 * Kiro Database Analyzer - JavaScript Edition
 * 
 * Analyzes Kiro CLI conversation database and prints detailed information
 * Usage: node kiro-analyzer.js [directory_path] [database_path]
 * 
 * Prerequisites: npm install sqlite3
 */

const sqlite3 = require('sqlite3').verbose();
const fs = require('fs');
const path = require('path');
const os = require('os');

// Console colors
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
  gray: '\x1b[90m',
  bold: '\x1b[1m',
};

function colorize(text, color) {
  return `${color}${text}${colors.reset}`;
}

function formatBox(title, width = 60) {
  const line = '─'.repeat(width);
  const padding = Math.max(0, width - title.length - 2);
  const leftPad = Math.floor(padding / 2);
  const rightPad = padding - leftPad;
  return `${line}\n${' '.repeat(leftPad)}${title}${' '.repeat(rightPad)}\n${line}`;
}

class KiroAnalyzer {
  constructor(dbPath) {
    this.dbPath = dbPath;
    this.db = new sqlite3.Database(dbPath, sqlite3.OPEN_READONLY, (err) => {
      if (err) {
        console.error(colorize('❌ Error opening database:', colors.red), err.message);
        process.exit(1);
      }
    });
  }

  /**
   * Find the default Kiro database location
   */
  static findDefaultDatabase() {
    const possiblePaths = [
      path.join(os.homedir(), '.local/share/kiro-cli/data.sqlite3'),
      path.join(os.homedir(), '.local/share/kiro/data.sqlite3'),
      path.join(os.homedir(), '.config/kiro/data.sqlite3'),
      './examples/data.sqlite3',
      './data.sqlite3',
    ];

    for (const dbPath of possiblePaths) {
      if (fs.existsSync(dbPath)) {
        return path.resolve(dbPath);
      }
    }
    return null;
  }

  /**
   * Get all conversations for a specific directory
   */
  async getConversations(directoryPath) {
    return new Promise((resolve, reject) => {
      const query = `
        SELECT key, conversation_id, value, created_at, updated_at 
        FROM conversations_v2 
        WHERE key = ? 
        ORDER BY created_at
      `;
      
      this.db.all(query, [directoryPath], (err, rows) => {
        if (err) reject(err);
        else resolve(rows || []);
      });
    });
  }

  /**
   * Get database statistics
   */
  async getDatabaseStats() {
    const tables = ['conversations_v2', 'migrations', 'auth_kv', 'state', 'history'];
    const stats = {};

    for (const table of tables) {
      const count = await new Promise((resolve, reject) => {
        this.db.get(`SELECT COUNT(*) as count FROM ${table}`, (err, row) => {
          if (err) reject(err);
          else resolve(row.count);
        });
      });
      stats[table] = count;
    }

    return stats;
  }

  /**
   * Get directory statistics
   */
  async getDirectoryStats() {
    return new Promise((resolve, reject) => {
      const query = `
        SELECT 
          key as directory,
          COUNT(*) as totalConversations,
          MIN(created_at) as firstActivity,
          MAX(updated_at) as lastActivity
        FROM conversations_v2 
        GROUP BY key 
        ORDER BY totalConversations DESC
      `;
      
      this.db.all(query, [], (err, rows) => {
        if (err) reject(err);
        else resolve(rows || []);
      });
    });
  }

  /**
   * Parse conversation JSON safely
   */
  parseConversationData(jsonString) {
    try {
      return JSON.parse(jsonString);
    } catch (error) {
      console.warn(colorize('⚠️  Failed to parse conversation data', colors.yellow));
      return null;
    }
  }

  /**
   * Extract user content as readable string
   */
  extractUserContent(content) {
    if (content.Prompt) {
      return content.Prompt.prompt;
    } else if (content.ToolUseResults) {
      const resultCount = content.ToolUseResults.tool_use_results.length;
      return `🔧 Tool results (${resultCount} tool(s) completed)`;
    }
    return '📝 Unknown content type';
  }

  /**
   * Extract assistant response as readable string
   */
  extractAssistantContent(response) {
    if (response.Response) {
      return {
        content: this.truncateText(response.Response.content, 200),
        isToolUse: false,
      };
    } else if (response.ToolUse) {
      const toolNames = response.ToolUse.tool_uses.map(tool => tool.name).join(', ');
      return {
        content: `🔧 Used tool(s): ${toolNames}`,
        isToolUse: true,
      };
    }
    return { content: '❓ Unknown response type', isToolUse: false };
  }

  /**
   * Truncate text for display
   */
  truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  }

  /**
   * Format timestamp
   */
  formatTimestamp(timestamp) {
    return new Date(timestamp).toLocaleString();
  }

  /**
   * Print database overview
   */
  async printDatabaseOverview() {
    console.log(colorize(formatBox('📄 Kiro Database Analysis'), colors.blue + colors.bold));
    console.log(colorize(`Database: ${this.dbPath}`, colors.gray));
    console.log();

    const stats = await this.getDatabaseStats();
    
    console.log(colorize('📊 Table Statistics:', colors.cyan + colors.bold));
    Object.entries(stats).forEach(([table, count]) => {
      const displayName = table.padEnd(20);
      console.log(`  ${displayName} ${colorize(count.toLocaleString().padStart(10), colors.green)}`);
    });
    console.log();
  }

  /**
   * Print directory statistics  
   */
  async printDirectoryStats() {
    console.log(colorize('📁 Directory Overview:', colors.magenta + colors.bold));
    console.log();

    const stats = await this.getDirectoryStats();
    
    if (stats.length === 0) {
      console.log(colorize('No conversations found in database.', colors.yellow));
      return;
    }

    stats.forEach((stat, index) => {
      console.log(colorize(`${index + 1}. ${this.truncateText(stat.directory, 50)}`, colors.cyan));
      console.log(`   ${colorize('Conversations:', colors.gray)} ${colorize(stat.totalConversations.toString(), colors.green)}`);
      console.log(`   ${colorize('First activity:', colors.gray)} ${this.formatTimestamp(stat.firstActivity)}`);
      console.log(`   ${colorize('Last activity:', colors.gray)} ${this.formatTimestamp(stat.lastActivity)}`);
      console.log();
    });
  }

  /**
   * Print conversation history for a directory
   */
  async printConversationHistory(directoryPath) {
    console.log(colorize(formatBox(`💬 Conversation History: ${path.basename(directoryPath)}`), colors.green + colors.bold));
    console.log(colorize(`Directory: ${directoryPath}`, colors.gray));
    console.log();

    const conversations = await this.getConversations(directoryPath);
    
    if (conversations.length === 0) {
      console.log(colorize('No conversations found for this directory.', colors.yellow));
      console.log();
      console.log(colorize('Available directories:', colors.cyan));
      const stats = await this.getDirectoryStats();
      stats.slice(0, 10).forEach(stat => {
        console.log(colorize(`  ${stat.directory}`, colors.gray));
      });
      return;
    }

    console.log(colorize(`✅ Found ${conversations.length} conversation(s)`, colors.green));
    console.log();

    for (const [index, conv] of conversations.entries()) {
      const conversationData = this.parseConversationData(conv.value);
      if (!conversationData) continue;

      console.log(colorize(`💬 Conversation ${index + 1}: ${conv.conversation_id.substring(0, 8)}...`, colors.magenta + colors.bold));
      console.log(`  ${colorize('Created:', colors.gray)} ${this.formatTimestamp(conv.created_at)}`);
      console.log(`  ${colorize('Messages:', colors.gray)} ${conversationData.history.length}`);
      
      if (conv.created_at !== conv.updated_at) {
        console.log(`  ${colorize('Updated:', colors.gray)} ${this.formatTimestamp(conv.updated_at)}`);
      }
      console.log();

      // Print each message exchange
      conversationData.history.forEach((exchange, msgIndex) => {
        // User message
        const userContent = this.extractUserContent(exchange.user.content);
        const userTime = new Date(exchange.user.timestamp).toLocaleTimeString();
        
        console.log(`   ${colorize('👤 User:', colors.green + colors.bold)} ${this.truncateText(userContent, 150)}`);
        console.log(`      ${colorize('🕒 ' + userTime, colors.gray)}`);

        // Assistant response
        const assistantResponse = this.extractAssistantContent(exchange.assistant);
        console.log(`   ${colorize('🤖 Assistant:', colors.cyan + colors.bold)} ${assistantResponse.content}`);

        // Performance metrics (first message only)
        if (msgIndex === 0 && exchange.request_metadata) {
          const responseTime = exchange.request_metadata.time_to_first_chunk?.secs || 0;
          const conversationType = exchange.request_metadata.chat_conversation_type;
          console.log(colorize(`      ⚡ Response time: ${responseTime}s (${conversationType})`, colors.gray));
        }

        console.log();
      });

      console.log(colorize('─'.repeat(60), colors.gray));
      console.log();
    }
  }

  /**
   * Close database connection
   */
  close() {
    this.db.close();
  }
}

// Main function
async function main() {
  const args = process.argv.slice(2);
  const directoryPath = args[0] || process.cwd();
  const dbPath = args[1];

  console.log(colorize('🚀 Kiro Database Analyzer - JavaScript Edition', colors.blue + colors.bold));
  console.log();

  // Find database
  let finalDbPath;
  if (dbPath) {
    if (!fs.existsSync(dbPath)) {
      console.error(colorize('❌ Database file not found:', colors.red), dbPath);
      process.exit(1);
    }
    finalDbPath = path.resolve(dbPath);
  } else {
    const defaultDb = KiroAnalyzer.findDefaultDatabase();
    if (!defaultDb) {
      console.error(colorize('❌ Could not find Kiro database.', colors.red));
      console.log(colorize('💡 Try specifying the database path as second argument.', colors.yellow));
      console.log(colorize('💡 Expected location: ~/.local/share/kiro-cli/data.sqlite3', colors.yellow));
      process.exit(1);
    }
    finalDbPath = defaultDb;
    console.log(colorize('✅ Found database:', colors.green), finalDbPath);
    console.log();
  }

  const analyzer = new KiroAnalyzer(finalDbPath);

  try {
    // Print database overview
    await analyzer.printDatabaseOverview();

    // Print directory statistics
    await analyzer.printDirectoryStats();

    // Print conversation history for specific directory
    const resolvedDirectory = path.resolve(directoryPath);
    await analyzer.printConversationHistory(resolvedDirectory);

  } catch (error) {
    console.error(colorize('❌ Error analyzing database:', colors.red), error);
    process.exit(1);
  } finally {
    analyzer.close();
  }
}

// Help function
function printHelp() {
  console.log(`
${colorize('Kiro Database Analyzer - JavaScript Edition', colors.blue + colors.bold)}

${colorize('Usage:', colors.cyan)}
  node kiro-analyzer.js [directory_path] [database_path]

${colorize('Arguments:', colors.cyan)}
  directory_path    Directory path to show conversations for (default: current directory)
  database_path     Path to Kiro SQLite database (default: auto-detected)

${colorize('Examples:', colors.cyan)}
  node kiro-analyzer.js                           # Analyze current directory
  node kiro-analyzer.js /home/user/project        # Analyze specific directory  
  node kiro-analyzer.js . ./examples/data.sqlite3 # Use specific database

${colorize('Prerequisites:', colors.cyan)}
  npm install sqlite3

${colorize('Features:', colors.cyan)}
  • Database overview and statistics
  • Directory-wise conversation analysis  
  • Detailed message history with timestamps
  • Tool usage tracking and performance metrics
  • Colored console output for readability
`);
}

// Handle help flag
if (process.argv.includes('--help') || process.argv.includes('-h')) {
  printHelp();
  process.exit(0);
}

// Run main function
if (require.main === module) {
  main().catch(console.error);
}

module.exports = { KiroAnalyzer };