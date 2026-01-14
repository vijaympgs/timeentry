/**
 * Org Chart Service - Local Employee Data Integration
 * Uses the generated 273 employee records for org chart display
 */

// Interface matching the expected OrgChartNode format
export interface OrgChartNode {
  id: string;
  employee_number: string;
  first_name: string;
  last_name: string;
  full_name: string;
  position_title: string;
  department_name: string;
  work_email: string;
  manager_name: string;
  is_active: boolean;
  children: OrgChartNode[];
}

interface GoJSNodeData {
  key: number;
  name: string;
  title: string;
  dept: string;
  pic: string;
  email: string;
  phone: string;
  parent?: number;
}

interface GoJSTreeModel {
  class: string;
  nodeDataArray: GoJSNodeData[];
}

interface HierarchyData {
  hierarchy: OrgChartNode[];
  total_employees: number;
  levels: number;
}

class OrgChartService {
  private employeeData: GoJSTreeModel | null = null;
  private hierarchyData: HierarchyData | null = null;

  /**
   * Load organization hierarchy data from backend API
   */
  async loadEmployeeData(): Promise<void> {
    try {
      const response = await fetch('/api/hrm/api/v1/organization-chart/hierarchy/');
      if (!response.ok) {
        throw new Error(`Failed to load organization hierarchy: ${response.status}`);
      }
      this.hierarchyData = await response.json();
    } catch (error) {
      console.error('Error loading organization hierarchy:', error);
      throw error;
    }
  }

  /**
   * Convert GoJS TreeModel format to OrgChartNode hierarchy
   */
  private convertToHierarchy(): HierarchyData {
    if (!this.employeeData) {
      throw new Error('Employee data not loaded');
    }

    const nodeMap = new Map<number, OrgChartNode>();
    const rootNodes: OrgChartNode[] = [];

    // First pass: create all nodes
    this.employeeData.nodeDataArray.forEach((employee: GoJSNodeData) => {
      const nameParts = employee.name.split(' ');
      const firstName = nameParts[0] || '';
      const lastName = nameParts.slice(1).join(' ') || '';

      const node: OrgChartNode = {
        id: employee.key.toString(),
        employee_number: `EMP${employee.key.toString().padStart(4, '0')}`,
        first_name: firstName,
        last_name: lastName,
        full_name: employee.name,
        position_title: employee.title,
        department_name: employee.dept,
        work_email: employee.email,
        manager_name: '', // Will be set in second pass
        is_active: true,
        children: []
      };

      nodeMap.set(employee.key, node);
    });

    // Second pass: establish parent-child relationships
    this.employeeData.nodeDataArray.forEach((employee: GoJSNodeData) => {
      const node = nodeMap.get(employee.key);
      if (!node) return;

      if (employee.parent) {
        const parentNode = nodeMap.get(employee.parent);
        if (parentNode) {
          node.manager_name = parentNode.full_name;
          parentNode.children.push(node);
        }
      } else {
        // This is a root node (CEO)
        rootNodes.push(node);
      }
    });

    // Calculate levels
    const calculateLevels = (nodes: OrgChartNode[], currentLevel: number = 1): number => {
      let maxLevel = currentLevel;
      nodes.forEach(node => {
        if (node.children.length > 0) {
          maxLevel = Math.max(maxLevel, calculateLevels(node.children, currentLevel + 1));
        }
      });
      return maxLevel;
    };

    const levels = calculateLevels(rootNodes);

    return {
      hierarchy: rootNodes,
      total_employees: this.employeeData.nodeDataArray.length,
      levels: levels
    };
  }

  /**
   * Get organizational hierarchy data for org chart
   */
  async getHierarchy(): Promise<HierarchyData> {
    if (!this.hierarchyData) {
      await this.loadEmployeeData();
    }
    return this.hierarchyData as HierarchyData;
  }

  /**
   * Get employee by ID
   */
  async getEmployeeById(id: string): Promise<OrgChartNode | null> {
    const hierarchy = await this.getHierarchy();
    
    const findNode = (nodes: OrgChartNode[]): OrgChartNode | null => {
      for (const node of nodes) {
        if (node.id === id) {
          return node;
        }
        if (node.children.length > 0) {
          const found = findNode(node.children);
          if (found) return found;
        }
      }
      return null;
    };

    return findNode(hierarchy.hierarchy);
  }

  /**
   * Search employees by name
   */
  async searchEmployees(query: string): Promise<OrgChartNode[]> {
    const hierarchy = await this.getHierarchy();
    const results: OrgChartNode[] = [];
    const lowerQuery = query.toLowerCase();

    const searchNodes = (nodes: OrgChartNode[]) => {
      nodes.forEach(node => {
        if (node.full_name.toLowerCase().includes(lowerQuery) ||
            node.position_title.toLowerCase().includes(lowerQuery) ||
            node.department_name.toLowerCase().includes(lowerQuery)) {
          results.push(node);
        }
        if (node.children.length > 0) {
          searchNodes(node.children);
        }
      });
    };

    searchNodes(hierarchy.hierarchy);
    return results;
  }

  /**
   * Get employees by department
   */
  async getEmployeesByDepartment(department: string): Promise<OrgChartNode[]> {
    const hierarchy = await this.getHierarchy();
    const results: OrgChartNode[] = [];

    const findInDepartment = (nodes: OrgChartNode[]) => {
      nodes.forEach(node => {
        if (node.department_name === department) {
          results.push(node);
        }
        if (node.children.length > 0) {
          findInDepartment(node.children);
        }
      });
    };

    findInDepartment(hierarchy.hierarchy);
    return results;
  }

  /**
   * Get all departments
   */
  async getDepartments(): Promise<string[]> {
    const hierarchy = await this.getHierarchy();
    const departments = new Set<string>();

    const collectDepartments = (nodes: OrgChartNode[]) => {
      nodes.forEach(node => {
        departments.add(node.department_name);
        if (node.children.length > 0) {
          collectDepartments(node.children);
        }
      });
    };

    collectDepartments(hierarchy.hierarchy);
    return Array.from(departments).sort();
  }

  /**
   * Clear cached data
   */
  clearCache(): void {
    this.employeeData = null;
    this.hierarchyData = null;
  }
}

export const orgChartService = new OrgChartService();
export default orgChartService;
