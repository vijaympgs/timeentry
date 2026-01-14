import React, { useEffect, useCallback } from "react";
import {
    Plus, Edit, Save, X, RotateCcw,
    CheckCircle, Send, Ban, FileEdit,
    Eye, Printer, Mail,
    ChevronFirst, ChevronLeft, ChevronRight, ChevronLast,
    RefreshCw, Trash2, PauseCircle, Octagon,
    Search, Filter,
    Upload, Download, Copy,
    StickyNote, Paperclip, Settings, HelpCircle, LogOut
} from "lucide-react";
import { useToolbarConfig, useToolbarPermissions } from "../../hooks/useToolbarConfig";

/**
 * MASTER TOOLBAR - BACKEND-DRIVEN CONFIGURATION
 * -------------------------------------------------
 * This component follows the new wiring specifications from 18_WIRING_CHECKLISTS
 * It is backend-driven, meaning the permissions and visible buttons are controlled
 * by a character-string configuration (e.g., "NRQFX") fetched via useToolbarConfig.
 */

export type MasterMode = "VIEW" | "EDIT" | "CREATE" | "VIEW_FORM";

interface MasterToolbarProps {
    viewId: string; // Must match ERPMenuItem.menu_id in database
    mode: MasterMode;
    onAction: (action: string) => void;
    hasSelection?: boolean;
}

interface ActionButton {
    id: string;
    icon: React.ElementType;
    label: string;
    shortcut: string;
    group: number;
    shortcutLabel: string;
    colorClass: string;
    permissionKey: keyof import("../../hooks/useToolbarConfig").ToolbarPermissions;
}

const ACTIONS: ActionButton[] = [
    // Group 1: CRUD Operations (from toolbar explorer)
    { id: 'new', icon: Plus, label: 'New', shortcut: 'F2', group: 1, shortcutLabel: 'F2', colorClass: 'text-blue-600', permissionKey: 'new' },
    { id: 'edit', icon: Edit, label: 'Edit', shortcut: 'F3', group: 1, shortcutLabel: 'F3', colorClass: 'text-blue-600', permissionKey: 'edit' },
    { id: 'view', icon: Eye, label: 'View', shortcut: 'F7', group: 1, shortcutLabel: 'F7', colorClass: 'text-indigo-600', permissionKey: 'view' },
    { id: 'delete', icon: Trash2, label: 'Delete', shortcut: 'F4', group: 1, shortcutLabel: 'F4', colorClass: 'text-red-600', permissionKey: 'delete' },
    { id: 'refresh', icon: RefreshCw, label: 'Refresh', shortcut: 'F9', group: 1, shortcutLabel: 'F9', colorClass: 'text-cyan-600', permissionKey: 'refresh' },
    { id: 'search', icon: Search, label: 'Search', shortcut: 'Ctrl+F', group: 1, shortcutLabel: 'Ctrl+F', colorClass: 'text-gray-600', permissionKey: 'search' },
    { id: 'filter', icon: Filter, label: 'Filter', shortcut: 'Alt+F', group: 1, shortcutLabel: 'Alt+F', colorClass: 'text-gray-600', permissionKey: 'filter' },
    { id: 'import', icon: Upload, label: 'Import', shortcut: 'Ctrl+I', group: 1, shortcutLabel: 'Ctrl+I', colorClass: 'text-violet-600', permissionKey: 'import' },
    { id: 'export', icon: Download, label: 'Export', shortcut: 'Ctrl+E', group: 1, shortcutLabel: 'Ctrl+E', colorClass: 'text-indigo-600', permissionKey: 'export' },
    { id: 'exit', icon: LogOut, label: 'Exit', shortcut: 'Esc', group: 1, shortcutLabel: 'ESC', colorClass: 'text-gray-600', permissionKey: 'exit' },
    // Group 2: Form Operations (for CREATE/EDIT modes)
    { id: 'save', icon: Save, label: 'Save', shortcut: 'F8', group: 2, shortcutLabel: 'F8', colorClass: 'text-emerald-600', permissionKey: 'save' },
    { id: 'cancel', icon: X, label: 'Cancel', shortcut: 'Esc', group: 2, shortcutLabel: 'ESC', colorClass: 'text-gray-600', permissionKey: 'cancel' },
    { id: 'clear', icon: RotateCcw, label: 'Clear', shortcut: 'F5', group: 2, shortcutLabel: 'F5', colorClass: 'text-amber-500', permissionKey: 'clear' },

    // Group 3: Workflow / Approval
    { id: 'authorize', icon: CheckCircle, label: 'Authorize', shortcut: 'F10', group: 3, shortcutLabel: 'F10', colorClass: 'text-green-600', permissionKey: 'authorize' },
    { id: 'submit', icon: Send, label: 'Submit', shortcut: 'Alt+S', group: 3, shortcutLabel: 'Alt+S', colorClass: 'text-blue-600', permissionKey: 'submit' },
    { id: 'reject', icon: Ban, label: 'Reject', shortcut: 'Alt+R', group: 3, shortcutLabel: 'Alt+R', colorClass: 'text-red-500', permissionKey: 'reject' },
    { id: 'amend', icon: FileEdit, label: 'Amend', shortcut: 'Alt+A', group: 3, shortcutLabel: 'Alt+A', colorClass: 'text-orange-600', permissionKey: 'amend' },

    // Group 4: Navigation
    { id: 'first', icon: ChevronFirst, label: 'First', shortcut: 'Home', group: 4, shortcutLabel: 'Home', colorClass: 'text-gray-600', permissionKey: 'first' },
    { id: 'prev', icon: ChevronLeft, label: 'Previous', shortcut: 'PgUp', group: 4, shortcutLabel: 'PgUp', colorClass: 'text-gray-600', permissionKey: 'prev' },
    { id: 'next', icon: ChevronRight, label: 'Next', shortcut: 'PgDn', group: 4, shortcutLabel: 'PgDn', colorClass: 'text-gray-600', permissionKey: 'next' },
    { id: 'last', icon: ChevronLast, label: 'Last', shortcut: 'End', group: 4, shortcutLabel: 'End', colorClass: 'text-gray-600', permissionKey: 'last' },

    // Group 5: Data Ops
    { id: 'hold', icon: PauseCircle, label: 'Hold', shortcut: 'Alt+H', group: 5, shortcutLabel: 'Alt+H', colorClass: 'text-yellow-600', permissionKey: 'hold' },
    { id: 'void', icon: Octagon, label: 'Void', shortcut: 'Alt+V', group: 5, shortcutLabel: 'Alt+V', colorClass: 'text-red-700', permissionKey: 'void' },

    // Group 6: Tools
    { id: 'notes', icon: StickyNote, label: 'Notes', shortcut: 'Alt+N', group: 6, shortcutLabel: 'Alt+N', colorClass: 'text-yellow-500', permissionKey: 'notes' },
    { id: 'attach', icon: Paperclip, label: 'Attach', shortcut: 'Alt+U', group: 6, shortcutLabel: 'Alt+U', colorClass: 'text-gray-500', permissionKey: 'attach' },
    { id: 'help', icon: HelpCircle, label: 'Help', shortcut: 'F1', group: 6, shortcutLabel: 'F1', colorClass: 'text-blue-500', permissionKey: 'help' },
];

export const MasterToolbar: React.FC<MasterToolbarProps> = ({
    viewId,
    mode,
    onAction,
    hasSelection = false
}) => {
    const { config, loading } = useToolbarConfig(viewId);

    const isActionDisabled = useCallback((action: ActionButton): boolean => {
        // 1. Loading guard
        if (!config) return action.id !== 'exit';

        // 2. Permission-based enable/disable (From character string logic in hook)
        if (!config.permissions[action.permissionKey]) return true;

        // 3. Mode-based state machine (Universal Guide Compliance)
        switch (mode) {
            case 'VIEW':
                // VIEW mode: NEVDXRQFZTJAPMI1234O (full listing mode functionality)
                return !['new', 'edit', 'view', 'delete', 'refresh', 'search', 'filter', 'exit', 'authorize', 'submit', 'reject', 'amend', 'print', 'email', 'import', 'export', 'first', 'prev', 'next', 'last', 'help', 'notes', 'attach'].includes(action.id);
            case 'VIEW_FORM':
                // VIEW_FORM mode: Only Exit button for modal forms
                return !['exit'].includes(action.id);
            case 'EDIT':
            case 'CREATE':
                // EDIT/CREATE mode: SCKX?BG
                return !['save', 'cancel', 'clear', 'exit', 'help', 'notes', 'attach'].includes(action.id);
            default:
                return false;
        }
    }, [mode, config]);

    const handleAction = useCallback((actionId: string) => {
        onAction(actionId);
    }, [onAction]);

    // Keyboard handling
    useEffect(() => {
        const handleKeyDown = (e: KeyboardEvent) => {
            const action = ACTIONS.find(a => {
                const parts = a.shortcut.split('+');
                return parts.every(part => {
                    if (part === 'ctrl') return e.ctrlKey;
                    if (part === 'alt') return e.altKey;
                    if (part === 'shift') return e.shiftKey;
                    return e.key.toLowerCase() === part.toLowerCase();
                });
            });

            if (action && !isActionDisabled(action)) {
                e.preventDefault();
                handleAction(action.id);
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [handleAction, isActionDisabled]);

    if (loading) return null;

    // If no config, don't render toolbar
    if (!config) return null;

    let currentGroup = 0;
    return (
        <div className="toolbar-container h-[42px] bg-gray-200 flex items-center gap-1 px-4">
            {ACTIONS.map((action) => {
                const disabled = isActionDisabled(action);
                const showSeparator = action.group !== currentGroup && currentGroup !== 0;
                currentGroup = action.group;

                // Only show actions that are permitted and not disabled
                if (!config.permissions[action.permissionKey] || disabled) {
                    return null;
                }

                return (
                    <React.Fragment key={action.id}>
                        {showSeparator && <div className="h-6 w-px bg-gray-400 mx-1" />}
                        <button
                            onClick={() => handleAction(action.id)}
                            disabled={disabled}
                        className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-none border-0 bg-transparent hover:bg-gray-300 transition-colors duration-180`}
                            title={`${action.label} (${action.shortcutLabel})`}
                        >
                            <action.icon className={`w-4 h-4 ${action.colorClass}`} />
                        </button>
                    </React.Fragment>
                );
            })}
            {/* Mode Display */}
            <div className="ml-auto pl-4 border-l border-gray-400">
                <span className="text-xs font-medium text-gray-700 bg-white px-2 py-1 rounded-none">
                    {mode === 'VIEW' ? 'LIST' : mode === 'VIEW_FORM' ? 'VIEW' : mode === 'CREATE' ? 'NEW' : mode}
                </span>
            </div>
        </div>
    );
};

// Export the old ToolbarButtons for backward compatibility
export const ToolbarButtons = {
    crud: (handlers: {
        onNew?: () => void
        onEdit?: () => void
        onView?: () => void
        onDelete?: () => void
    }) => [
        { id: 'new', icon: Plus, label: 'New', onClick: handlers.onNew || (() => {}), variant: 'primary' as const },
        { id: 'edit', icon: Edit, label: 'Edit', onClick: handlers.onEdit || (() => {}) },
        { id: 'view', icon: Eye, label: 'View', onClick: handlers.onView || (() => {}) },
        { id: 'delete', icon: Trash2, label: 'Delete', onClick: handlers.onDelete || (() => {}), variant: 'danger' as const }
    ],
    data: (handlers: {
        onRefresh?: () => void
        onClear?: () => void
        onExport?: () => void
        onImport?: () => void
    }) => [
        { id: 'refresh', icon: RefreshCw, label: 'Refresh', onClick: handlers.onRefresh || (() => {}) },
        { id: 'clear', icon: X, label: 'Clear', onClick: handlers.onClear || (() => {}) },
        { id: 'export', icon: Download, label: 'Export', onClick: handlers.onExport || (() => {}) },
        { id: 'import', icon: Upload, label: 'Import', onClick: handlers.onImport || (() => {}) }
    ],
    search: (handlers: {
        onSearch?: () => void
        onFilter?: () => void
    }) => [
        { id: 'search', icon: Search, label: 'Search', onClick: handlers.onSearch || (() => {}) },
        { id: 'filter', icon: Filter, label: 'Filter', onClick: handlers.onFilter || (() => {}) }
    ],
    form: (handlers: {
        onSave?: () => void
        onCancel?: () => void
        onClone?: () => void
    }) => [
        { id: 'save', icon: Save, label: 'Save', onClick: handlers.onSave || (() => {}), variant: 'primary' as const },
        { id: 'cancel', icon: X, label: 'Cancel', onClick: handlers.onCancel || (() => {}) },
        { id: 'clone', icon: Copy, label: 'Clone', onClick: handlers.onClone || (() => {}) }
    ],
    auth: (handlers: {
        onAuthorize?: () => void
        onExit?: () => void
    }) => [
        { id: 'authorize', icon: CheckCircle, label: 'Authorize', onClick: handlers.onAuthorize || (() => {}), variant: 'primary' as const },
        { id: 'exit', icon: LogOut, label: 'Exit', onClick: handlers.onExit || (() => {}) }
    ]
};
