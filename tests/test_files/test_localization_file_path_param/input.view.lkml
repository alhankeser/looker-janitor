view: orders {
  sql_table_name: `my_project.dataset.orders` ;;

  dimension: c_dimension_name {
    type: number
  }
  
  dimension: d_dimension_name {
    type: number
    label: "orders.d_dimension_name.label"
  }

  dimension: z_dimension_name {
    type: number
    label: "a_dimension_name"
  }
 
  measure: a_measure_name {
    type: average
  }

  filter: a_filter_name {
    type: number
  }
}
