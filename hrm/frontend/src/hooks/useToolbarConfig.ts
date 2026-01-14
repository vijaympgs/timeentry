import { useState, useEffect } from 'react';

export interface ToolbarPermissions {
  new: boolean;
  edit: boolean;
  refresh: boolean;
  search: boolean;
  filter: boolean;
  exit: boolean;
  view: boolean;
  delete: boolean;
  import: boolean;
  export: boolean;
  clone: boolean;
  notes: boolean;
  attach: boolean;
  help: boolean;
  save: boolean;
  cancel: boolean;
  clear: boolean;
  authorize: boolean;
  submit: boolean;
  reject: boolean;
  amend: boolean;
  print: boolean;
  email: boolean;
  first: boolean;
  prev: boolean;
  next: boolean;
  last: boolean;
  hold: boolean;
  void: boolean;
}

interface ToolbarConfigResponse {
  permissions: ToolbarPermissions;
  config: string;
}

// Feature flag for API-driven vs fallback system
const USE_NEW_PERMISSION_SYSTEM = true;

export const useToolbarConfig = (viewId: string) => {
  const [config, setConfig] = useState<ToolbarConfigResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchToolbarConfig = async () => {
      try {
        setLoading(true);
        
        if (USE_NEW_PERMISSION_SYSTEM) {
          // NEW: API-driven system - fetch filtered actions from backend
          // Note: This would be the correct implementation, but for now we'll use the existing endpoint
          const response = await fetch(`http://localhost:8000/api/toolbar-permissions/?view_id=${viewId}&mode=VIEW`, {
            headers: {
              'Authorization': `Bearer ${getAuthToken()}`,
            }
          });
          
          if (!response.ok) {
            throw new Error(`Toolbar permissions not found for viewId: ${viewId}`);
          }
          
          const data = await response.json();
          setConfig({
            permissions: convertActionsToPermissions(data.allowed_actions),
            config: data.toolbar_config || '',
          });
        } else {
          // OLD: Character-based system - fetch character string and parse frontend
          const response = await fetch(`http://localhost:8000/api/toolbar-config/${viewId}/`);
          if (!response.ok) {
            throw new Error(`Toolbar config not found for viewId: ${viewId}`);
          }
          
          const data = await response.json();
          setConfig({
            permissions: parseConfigString(data.toolbar_config),
            config: data.toolbar_config,
          });
        }
      } catch (error) {
        console.error('Failed to fetch toolbar config:', error);
        // No fallback - set config to null if not found in Django
        setConfig(null);
      } finally {
        setLoading(false);
      }
    };

    fetchToolbarConfig();
  }, [viewId]);

  return { config, loading };
};

// Helper function to get auth token (placeholder - implement based on your auth system)
const getAuthToken = (): string => {
  // This should return the authentication token from your auth system
  // For now, return empty string - implement based on your authentication mechanism
  return localStorage.getItem('authToken') || '';
};

// Helper function to convert API action array to permissions object
const convertActionsToPermissions = (allowedActions: string[]): ToolbarPermissions => {
  const permissions: ToolbarPermissions = {
    new: false,
    edit: false,
    refresh: false,
    search: false,
    filter: false,
    exit: false,
    view: false,
    delete: false,
    import: false,
    export: false,
    clone: false,
    notes: false,
    attach: false,
    help: false,
    save: false,
    cancel: false,
    clear: false,
    authorize: false,
    submit: false,
    reject: false,
  amend: false,
    print: false,
    email: false,
    first: false,
    prev: false,
    next: false,
    last: false,
    hold: false,
    void: false,
  };

  const actionMap: Record<string, keyof ToolbarPermissions> = {
    'new': 'new',
    'edit': 'edit',
    'view': 'view',
    'delete': 'delete',
    'refresh': 'refresh',
    'search': 'search',
    'filter': 'filter',
    'exit': 'exit',
    'import': 'import',
    'export': 'export',
    'clone': 'clone',
    'notes': 'notes',
    'attach': 'attach',
    'help': 'help',
    'save': 'save',
    'cancel': 'cancel',
    'clear': 'clear',
    'authorize': 'authorize',
    'submit': 'submit',
    'reject': 'reject',
    'amend': 'amend',
    'print': 'print',
    'email': 'email',
    'first': 'first',
    'previous': 'prev',
    'next': 'next',
    'last': 'last',
    'hold': 'hold',
    'void': 'void',
  };

  for (const action of allowedActions) {
    if (actionMap[action]) {
      permissions[actionMap[action]] = true;
    }
  }

  return permissions;
};

// Helper function to parse character string to permissions (fallback)
const parseConfigString = (configString: string): ToolbarPermissions => {
  const permissions: ToolbarPermissions = {
    new: false,
    edit: false,
    refresh: false,
    search: false,
    filter: false,
    exit: false,
    view: false,
    delete: false,
    import: false,
    export: false,
    clone: false,
    notes: false,
    attach: false,
    help: false,
    save: false,
    cancel: false,
    clear: false,
    authorize: false,
    submit: false,
    reject: false,
  amend: false,
    print: false,
    email: false,
    first: false,
    prev: false,
    next: false,
    last: false,
    hold: false,
    void: false,
  };

  const actionMap: Record<string, keyof ToolbarPermissions> = {
    'N': 'new',
    'E': 'edit',
    'R': 'refresh',
    'Q': 'search',
    'F': 'filter',
    'X': 'exit',
    'V': 'view',
    'D': 'delete',
    'I': 'import',
    'O': 'export',
    'L': 'clone',
    'B': 'notes',
    'U': 'attach',
    'G': 'help',
    'S': 'save',
    'C': 'cancel',
    'K': 'clear',
    'A': 'authorize',
    'T': 'submit',
    'J': 'reject',
    'W': 'amend',
    'P': 'print',
    'M': 'email',
    '1': 'first',
    '2': 'prev',
    '3': 'next',
    '4': 'last',
    'H': 'hold',
    'Z': 'void',
  };

  for (const char of configString.toUpperCase()) {
    if (actionMap[char]) {
      permissions[actionMap[char]] = true;
    }
  }

  return permissions;
};

// Export the new useToolbarPermissions hook for API-driven system
export const useToolbarPermissions = (viewId: string, mode: string, skip: boolean = false) => {
  const [allowedActions, setAllowedActions] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (skip) {
      setLoading(false);
      return;
    }

    const fetchPermissions = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const response = await fetch(
          `/api/toolbar-permissions/?view_id=${viewId}&mode=${mode}`,
          {
            headers: {
              'Authorization': `Bearer ${getAuthToken()}`,
            }
          }
        );

        if (!response.ok) {
          throw new Error(`Toolbar permissions not found for viewId: ${viewId}, mode: ${mode}`);
        }

        const data = await response.json();
        setAllowedActions(data.allowed_actions);
        setLoading(false);
      } catch (err) {
        setError('Failed to load toolbar permissions');
        setLoading(false);
      }
    };

    fetchPermissions();
  }, [viewId, mode, skip]);

  return { allowedActions, loading, error };
};
