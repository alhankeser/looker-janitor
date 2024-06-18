view: orders {
  sql_table_name: `my_project.dataset.orders` ;;

  filter: a_filter_name {
    type: number
  }

  dimension: a_dimension_name {
    type: number
    sql: ${TABLE}."a_dimension_name" ;;
  }

  measure: a_measure_name {
    type: average
    sql: ${TABLE}."a_dimension_name" ;;
    filters: [something: "Yes"]
  }
}
