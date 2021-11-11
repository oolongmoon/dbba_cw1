g_last_week: nx.DiGraph = G_dic[date_list[-1]]

partition_bit = louvain.best_partition(g_last_week.to_undirected())
partition_df = pd.DataFrame.from_dict(partition_bit, orient='index').reset_index()
partition_df.columns = ['node', 'community']

edg_list_df = nx.to_pandas_edgelist(g_last_week)
edg_list_df: pd.DataFrame = edg_list_df[['source', 'target']]
super_edge_df = pd.merge(
    edg_list_df,
    partition_df.rename(columns={'node': 'source', 'community': 'community_source'}),
    on='source', how='left'
)
super_edge_df = pd.merge(
    super_edge_df,
    partition_df.rename(columns={'node': 'target', 'community': 'community_target'}),
    on='target', how='left'
)
super_edge_df['edge'] = list(zip(super_edge_df['community_source'], super_edge_df['community_target']))

df_super_edge_list = pd.DataFrame(columns=['source', 'target', 'weight'],
                                  data=[
                                      [edge_i[0], edge_i[1], len(df_i)]
                                      for edge_i, df_i in super_edge_df.groupby(['edge'])
                                  ])

df_node_weight = \
    df_super_edge_list[df_super_edge_list['source'] == df_super_edge_list['target']] \
    .drop(['target'], axis='columns')
df_node_weight['weight_adjust'] = 200 * (np.log(df_node_weight['weight']) / max(np.log(df_node_weight['weight'])))

df_super_edge_list.drop(index=df_node_weight.index, inplace=True)

df_super_edge_list['weight_adjust'] = 1 - np.exp(-df_super_edge_list['weight'])
# Super-network
super_network = nx.from_pandas_edgelist(df_super_edge_list,
                                        source='source',
                                        target='target',
                                        edge_attr=True,
                                        create_using=nx.DiGraph)