view: orders {
  sql_table_name: `my_project.dataset.orders` ;;

  filter: a_filter_name {
    type: number
  }

  dimension: z_dimension_name {
    type: number
    label: "a_dimension_name"
  }

  dimension: d_dimension_name {
    type: number
    label: "orders.d_dimension_name.label"
  }

  dimension: c_dimension_name {
    type: number
  }

  measure: a_measure_name {
    type: average
  }
}
