import React from 'react'
import { ChevronLeft, ChevronRight, ChevronsUpDown, ChevronDown, ChevronUp } from 'lucide-react'

interface Column<T> {
  key: string
  title: string
  dataIndex: keyof T
  sortable?: boolean
  width?: string
  render?: (value: any, record: T) => React.ReactNode
}

interface DataTableProps<T> {
  data: T[]
  columns: Column<T>[]
  onRowClick?: (record: T) => void
  onSort?: (column: Column<T>, direction: 'asc' | 'desc') => void
  loading?: boolean
  pagination?: {
    current: number
    pageSize: number
    total: number
    onChange: (page: number, pageSize: number) => void
  }
  selectable?: boolean
  onSelectionChange?: (selectedRows: T[]) => void
}

export function DataTable<T extends Record<string, any>>({
  data,
  columns,
  onRowClick,
  onSort,
  loading = false,
  pagination,
  selectable = false,
  onSelectionChange
}: DataTableProps<T>) {
  const [sortColumn, setSortColumn] = React.useState<keyof T | null>(null)
  const [sortDirection, setSortDirection] = React.useState<'asc' | 'desc'>('asc')
  const [selectedRows, setSelectedRows] = React.useState<T[]>([])

  const handleSort = (column: Column<T>) => {
    if (column.sortable) {
      const newDirection = sortColumn === column.dataIndex && sortDirection === 'asc' ? 'desc' : 'asc'
      setSortColumn(column.dataIndex)
      setSortDirection(newDirection)
      onSort?.(column, newDirection)
    }
  }

  const handleRowSelect = (record: T) => {
    const isSelected = selectedRows.some(row => 
      JSON.stringify(row) === JSON.stringify(record)
    )
    
    if (isSelected) {
      setSelectedRows(selectedRows.filter(row => 
        JSON.stringify(row) !== JSON.stringify(record)
      ))
    } else {
      setSelectedRows([...selectedRows, record])
    }
    onSelectionChange?.(selectedRows)
  }

  const handleSelectAll = () => {
    if (selectedRows.length === data.length) {
      setSelectedRows([])
    } else {
      setSelectedRows([...data])
    }
    onSelectionChange?.(data)
  }

  const sortedData = React.useMemo(() => {
    if (!sortColumn) return data

    return [...data].sort((a, b) => {
      const aValue = a[sortColumn]
      const bValue = b[sortColumn]

      if (aValue < bValue) return sortDirection === 'asc' ? -1 : 1
      if (aValue > bValue) return sortDirection === 'asc' ? 1 : -1
      return 0
    })
  }, [data, sortColumn, sortDirection])

  const getSortIcon = (column: Column<T>) => {
    if (sortColumn !== column.dataIndex) {
      return <ChevronsUpDown className="h-4 w-4" />
    }
    return sortDirection === 'asc' ? 
      <ChevronUp className="h-4 w-4" /> : 
      <ChevronDown className="h-4 w-4" />
  }

  return (
    <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
      {/* Table Header */}
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              {selectable && (
                <th className="px-6 py-3 text-left">
                  <input
                    type="checkbox"
                    checked={selectedRows.length === data.length && data.length > 0}
                    onChange={handleSelectAll}
                    className="h-4 w-4 text-blue-600 rounded border-gray-300"
                  />
                </th>
              )}
              {columns.map((column) => (
                <th
                  key={column.key}
                  onClick={() => column.sortable && handleSort(column)}
                  className={`px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider ${
                    column.sortable ? 'cursor-pointer hover:bg-gray-100' : ''
                  }`}
                  style={{ width: column.width }}
                >
                  <div className="flex items-center gap-2">
                    {column.title}
                    {column.sortable && (
                      <span className="ml-1">
                        {getSortIcon(column)}
                      </span>
                    )}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {loading ? (
              <tr>
                <td colSpan={columns.length + (selectable ? 1 : 0)} className="px-6 py-4 text-center text-gray-500">
                  Loading...
                </td>
              </tr>
            ) : (
              sortedData.map((record, index) => (
                <tr
                  key={index}
                  onClick={() => onRowClick?.(record)}
                  className={`hover:bg-gray-50 cursor-pointer ${
                    selectedRows.some(row => JSON.stringify(row) === JSON.stringify(record))
                      ? 'bg-blue-50'
                      : ''
                  }`}
                >
                  {selectable && (
                    <td className="px-6 py-4">
                      <input
                        type="checkbox"
                        checked={selectedRows.some(row => 
                          JSON.stringify(row) === JSON.stringify(record)
                        )}
                        onChange={() => handleRowSelect(record)}
                        className="h-4 w-4 text-blue-600 rounded border-gray-300"
                      />
                    </td>
                  )}
                  {columns.map((column) => (
                    <td
                      key={column.key}
                      className="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                      style={{ width: column.width }}
                    >
                      {column.render 
                        ? column.render(record[column.dataIndex], record)
                        : record[column.dataIndex]
                      }
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {pagination && (
        <div className="px-6 py-3 bg-gray-50 border-t border-gray-200 flex items-center justify-between">
          <div className="text-sm text-gray-700">
            Showing {((pagination.current - 1) * pagination.pageSize) + 1} to{' '}
            {Math.min(pagination.current * pagination.pageSize, pagination.total)} of{' '}
            {pagination.total} results
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => pagination.onChange(1, pagination.pageSize)}
              disabled={pagination.current === 1}
              className="px-3 py-1 text-sm text-gray-500 hover:text-gray-700 disabled:opacity-50"
            >
              <ChevronLeft className="h-4 w-4" />
            </button>
            <button
              onClick={() => pagination.onChange(
                Math.max(1, pagination.current - 1),
                pagination.pageSize
              )}
              disabled={pagination.current === 1}
              className="px-3 py-1 text-sm text-gray-500 hover:text-gray-700 disabled:opacity-50"
            >
              Previous
            </button>
            
            <span className="px-3 py-1 text-sm text-gray-700">
              Page {pagination.current} of {Math.ceil(pagination.total / pagination.pageSize)}
            </span>
            
            <button
              onClick={() => pagination.onChange(
                Math.min(
                  Math.ceil(pagination.total / pagination.pageSize),
                  pagination.current + 1
                ),
                pagination.pageSize
              )}
              disabled={pagination.current === Math.ceil(pagination.total / pagination.pageSize)}
              className="px-3 py-1 text-sm text-gray-500 hover:text-gray-700 disabled:opacity-50"
            >
              Next
            </button>
            <button
              onClick={() => pagination.onChange(
                Math.ceil(pagination.total / pagination.pageSize),
                pagination.pageSize
              )}
              disabled={pagination.current === Math.ceil(pagination.total / pagination.pageSize)}
              className="px-3 py-1 text-sm text-gray-500 hover:text-gray-700 disabled:opacity-50"
            >
              <ChevronRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
